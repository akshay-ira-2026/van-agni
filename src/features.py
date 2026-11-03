"""Van Agni feature builder: one row per grid cell per day.
Label: did NASA FIRMS (Fire Information for Resource Management System) see a
vegetation fire in this cell in the NEXT 7 days (day+1 .. day+7)?"""
import numpy as np, pandas as pd
LAT0, LON0, S = 28.75, 77.5, 0.25   # 0.25 degree grid (about 27 km) over Uttarakhand
HORIZON = 7

def load_fires(path):
    f = pd.read_csv(path)
    f = f[(f['type'] == 0) & (f['confidence'] >= 30)]        # type 0 = presumed vegetation fire
    f['clat'] = (np.floor((f.latitude - LAT0) / S) * S + LAT0 + S / 2).round(3)
    f['clon'] = (np.floor((f.longitude - LON0) / S) * S + LON0 + S / 2).round(3)
    f['date'] = pd.to_datetime(f.acq_date)
    return f

def build(grid, weather, fires):
    g = grid[grid.elev >= 500][['cell', 'lat', 'lon', 'elev']]
    w = weather.copy()
    w['date'] = pd.to_datetime(w['date'].astype(str), format='%Y%m%d')
    w = w.replace(-999.0, np.nan).sort_values(['cell', 'date'])
    w = w.merge(g, on='cell')
    grp = w.groupby('cell')
    w['rain'] = w.PRECTOTCORR
    w['rain7'] = grp.rain.transform(lambda s: s.rolling(7, 1).sum())
    w['rain30'] = grp.rain.transform(lambda s: s.rolling(30, 1).sum())
    w['rain90'] = grp.rain.transform(lambda s: s.rolling(90, 1).sum())
    wet = (w.rain >= 1.0).astype(int)
    w['dry_days'] = wet.groupby(w.cell).transform(lambda s: s.groupby(s.cumsum()).cumcount())
    w['tmax7'] = grp.T2M_MAX.transform(lambda s: s.rolling(7, 1).mean())
    w['rh7'] = grp.RH2M.transform(lambda s: s.rolling(7, 1).mean())
    w['doy'] = w.date.dt.dayofyear
    w['month'] = w.date.dt.month
    # fires seen in the cell in the last 7 days (persistence signal)
    fc = fires.groupby(['clat', 'clon', 'date']).size().rename('n').reset_index()
    fc = fc.merge(g, left_on=['clat', 'clon'], right_on=['lat', 'lon'])[['cell', 'date', 'n']]
    w = w.merge(fc, on=['cell', 'date'], how='left').fillna({'n': 0})
    grp = w.groupby('cell')
    w['fires_past7'] = grp.n.transform(lambda s: s.rolling(7, 1).sum())
    # label: any fire in next 7 days
    fut = grp.n.transform(lambda s: s[::-1].rolling(HORIZON, 1).sum()[::-1].shift(-1))
    w['y'] = (fut > 0).astype(int)
    w.loc[fut.isna(), 'y'] = np.nan
    return w.dropna(subset=['y'])

FEATURES = ['T2M_MAX', 'RH2M', 'WS10M_MAX', 'rain7', 'rain30', 'rain90', 'dry_days',
            'tmax7', 'rh7', 'doy', 'elev', 'lat', 'lon', 'fires_past7', 'hist_rate']

def add_history(df, train_years):
    """Historic fire rate per cell, from training years only (no leakage)."""
    tr = df[df.date.dt.year.isin(train_years)]
    rate = tr.groupby('cell').n.apply(lambda s: (s > 0).mean()).rename('hist_rate')
    return df.drop(columns=['hist_rate'], errors='ignore').merge(rate, on='cell', how='left').fillna({'hist_rate': 0})
