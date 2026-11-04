"""Score every grid cell. Mode 'live': Open-Meteo forecast (past 92 days + today) + NASA FIRMS last 7 days.
Mode 'replay YYYY-MM-DD': score a past day from the archive data, for the demo."""
import sys, json, io, socket, time, numpy as np, pandas as pd, requests, joblib
import urllib3.util.connection as _uc
_uc.allowed_gai_family = lambda: socket.AF_INET  # runners sometimes have no IPv6 route (Errno 101)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
HTTP = requests.Session()
HTTP.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=3, status_forcelist=[429, 500, 502, 503, 504])))
FIRMS_URLS = ['https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_Asia_7d.csv',
              'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_Asia_7d.csv',
              'https://firms2.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_Asia_7d.csv']
FIRE_SOURCE = 'none'

def fetch_firms():
    global FIRE_SOURCE
    for u in FIRMS_URLS:
        for k in range(3):
            try:
                r = HTTP.get(u, timeout=120); r.raise_for_status()
                f = pd.read_csv(io.StringIO(r.text))
                if {'latitude', 'longitude', 'acq_date'} <= set(f.columns):
                    FIRE_SOURCE = u.split('/')[-1]; return f
            except Exception as e:
                print('FIRMS fetch failed', u, k, e, file=sys.stderr); time.sleep(10)
    print('FIRMS unavailable: scoring on weather and history only', file=sys.stderr)
    return pd.DataFrame(columns=['latitude', 'longitude', 'acq_date', 'confidence'])
sys.path.insert(0, 'src'); from features import *; from alerts import alert
model = joblib.load('outputs/van_agni_lgbm.joblib')
grid = pd.read_csv('data/grid.csv'); g = grid[grid.elev >= 500].reset_index(drop=True)
TRAIN = [2019, 2020, 2021, 2022, 2023]

def hist_rates():
    w = pd.read_csv('data/weather_power_daily_2019_2025.csv.gz')
    fires = load_fires('data/firms_modis_uttarakhand_2019_2025.csv')
    df = build(grid, w, fires); df = add_history(df, TRAIN)
    return df

def live():
    rows = []
    for i in range(0, len(g), 50):
        ch = g.iloc[i:i+50]
        j = HTTP.get('https://api.open-meteo.com/v1/forecast', params={'latitude': ','.join(map(str, ch.lat)), 'longitude': ','.join(map(str, ch.lon)),
            'daily': 'temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum', 'past_days': 92, 'forecast_days': 1,
            'timezone': 'Asia/Kolkata', 'wind_speed_unit': 'ms'}, timeout=120).json()
        if isinstance(j, dict): j = [j]
        for (_, c), d in zip(ch.iterrows(), j):
            x = pd.DataFrame(d['daily']); x['cell'] = c.cell; rows.append(x)
    w = pd.concat(rows).rename(columns={'temperature_2m_max': 'T2M_MAX', 'relative_humidity_2m_mean': 'RH2M', 'wind_speed_10m_max': 'WS10M_MAX', 'precipitation_sum': 'PRECTOTCORR', 'time': 'date'})
    w['date'] = w.date.str.replace('-', '')
    f = fetch_firms(); f['type'] = 0
    f['latitude'] = pd.to_numeric(f.latitude, errors='coerce'); f['longitude'] = pd.to_numeric(f.longitude, errors='coerce')
    f = f[(f.latitude.between(28.75, 31.5)) & (f.longitude.between(77.5, 81.0))]
    f['confidence'] = pd.to_numeric(f.confidence, errors='coerce').fillna(50)
    fires = load_fires_df(f)
    df = build_nolabel(grid, w, fires)
    hr = hist_rates().groupby('cell').hist_rate.first()
    df = df.merge(hr, on='cell', how='left').fillna({'hist_rate': 0})
    return df[df.date == df.date.max()]

def load_fires_df(f):
    f['clat'] = (np.floor((f.latitude - LAT0) / S) * S + LAT0 + S / 2).round(3)
    f['clon'] = (np.floor((f.longitude - LON0) / S) * S + LON0 + S / 2).round(3)
    f['date'] = pd.to_datetime(f.acq_date); return f

def build_nolabel(grid, w, fires):
    w = w.copy(); w['y_dummy'] = 0
    import features as F
    old = F.HORIZON
    d = F.build(grid, pd.concat([w, w.assign(date=(pd.to_datetime(w.date) + pd.Timedelta(days=0)).dt.strftime('%Y%m%d'))]).drop_duplicates(['cell', 'date']), fires) if False else None
    # same feature code as training, without needing future days for a label
    w['date'] = pd.to_datetime(w['date'].astype(str), format='%Y%m%d')
    w = w.sort_values(['cell', 'date']).merge(grid[grid.elev >= 500][['cell', 'lat', 'lon', 'elev']], on='cell')
    gp = w.groupby('cell'); w['rain'] = w.PRECTOTCORR.fillna(0)
    for k in (7, 30, 90): w['rain%d' % k] = gp.rain.transform(lambda s: s.rolling(k, 1).sum())
    wet = (w.rain >= 1.0).astype(int)
    w['dry_days'] = wet.groupby(w.cell).transform(lambda s: s.groupby(s.cumsum()).cumcount())
    w['tmax7'] = gp.T2M_MAX.transform(lambda s: s.rolling(7, 1).mean()); w['rh7'] = gp.RH2M.transform(lambda s: s.rolling(7, 1).mean())
    w['doy'] = w.date.dt.dayofyear; w['month'] = w.date.dt.month
    fc = fires.groupby(['clat', 'clon', 'date']).size().rename('n').reset_index()
    fc = fc.merge(grid, left_on=['clat', 'clon'], right_on=['lat', 'lon'])[['cell', 'date', 'n']]
    w = w.merge(fc, on=['cell', 'date'], how='left').fillna({'n': 0})
    w['fires_past7'] = w.groupby('cell').n.transform(lambda s: s.rolling(7, 1).sum())
    return w

def replay(day):
    df = hist_rates(); return df[df.date == pd.Timestamp(day)]

if __name__ == '__main__':
    mode = sys.argv[1]
    d = live() if mode == 'live' else replay(sys.argv[2])
    d = d.assign(p=model.predict_proba(d[FEATURES])[:, 1]).sort_values('p', ascending=False)
    day = str(pd.Timestamp(d.date.max()).date())
    top = []
    for _, r in d.head(10).iterrows():
        e, h = alert(r.to_dict()); top.append({'cell': int(r.cell), 'lat': r.lat, 'lon': r.lon, 'p': round(float(r.p), 3), 'en': e, 'hi': h})
    cells = d[['cell', 'lat', 'lon', 'p', 'dry_days', 'rh7', 'T2M_MAX', 'fires_past7']].round(3).to_dict('records')
    out = {'mode': mode, 'date': day, 'cells': cells, 'top10': top}
    if mode != 'live':
        out['actual_fire_cells_next7'] = d[d.y == 1].cell.astype(int).tolist()
    name = 'live' if mode == 'live' else 'replay_' + day
    json.dump(out, open('docs/%s.json' % name, 'w'), ensure_ascii=False, indent=1, default=float)
    print(name, day, 'top:', [(t['cell'], t['p']) for t in top[:5]])
    print(top[0]['en']); print(top[0]['hi'])
    if mode != 'live':
        hit = len(set(t['cell'] for t in top) & set(out['actual_fire_cells_next7']))
        print('replay: actual fire cells next 7d =', len(out['actual_fire_cells_next7']), 'caught in top10 =', hit)
