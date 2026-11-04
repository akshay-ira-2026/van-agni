"""Train + back-test Van Agni. Train 2019-2023, validate 2024, test 2025 (fire season Feb-Jun).
Energy/carbon measured with CodeCarbon."""
import json, sys, time, numpy as np, pandas as pd, lightgbm as lgb, joblib
from sklearn.metrics import roc_auc_score, average_precision_score
from codecarbon import OfflineEmissionsTracker
sys.path.insert(0, 'src'); from features import *

grid = pd.read_csv('data/grid.csv')
weather = pd.read_csv('data/weather_power_daily_2019_2025.csv.gz')
fires = load_fires('data/firms_modis_uttarakhand_2019_2025.csv')
df = build(grid, weather, fires)
df = add_viirs(df, grid, load_viirs_df(pd.read_csv('data/firms_viirs_snpp_uttarakhand_2019_2025.csv.gz')))
TRAIN = [2019, 2020, 2021, 2022, 2023]
df = add_history(df, TRAIN)
yr = df.date.dt.year
tr, va, te = df[yr.isin(TRAIN)], df[yr == 2024], df[yr == 2025]

tracker = OfflineEmissionsTracker(country_iso_code='IND', project_name='van-agni-train',
                                  output_dir='outputs', output_file='codecarbon_train.csv', log_level='error')
tracker.start(); t0 = time.time()
model = lgb.LGBMClassifier(n_estimators=400, learning_rate=0.03, num_leaves=31, min_child_samples=50,
                           subsample=0.8, subsample_freq=1, colsample_bytree=0.8, verbose=-1)
model.fit(tr[FEATURES], tr.y, eval_set=[(va[FEATURES], va.y)], callbacks=[lgb.early_stopping(40, verbose=False)])
train_s = time.time() - t0; train_kg = tracker.stop()

def season_eval(d, name):
    p = model.predict_proba(d[FEATURES])[:, 1]
    d = d.assign(p=p)
    s = d[d.month.between(2, 6)]
    out = {'rows': int(len(d)), 'auc': round(roc_auc_score(d.y, d.p), 3),
           'pr_auc': round(average_precision_score(d.y, d.p), 3),
           'season_auc': round(roc_auc_score(s.y, s.p), 3), 'base_rate': round(float(d.y.mean()), 3)}
    # operational metric: each day, patrol top 10 cells. share of next-7-day fire cells caught
    caught = tot = 0; cb = 0
    for day, x in s.groupby('date'):
        pos = x[x.y == 1]
        if len(pos) == 0: continue
        top = set(x.nlargest(10, 'p').cell); topb = set(x.nlargest(10, 'hist_rate').cell)
        caught += len(top & set(pos.cell)); cb += len(topb & set(pos.cell)); tot += len(pos)
    out['top10_recall'] = round(caught / tot, 3); out['baseline_top10_recall_hist_only'] = round(cb / tot, 3)
    # rule baseline: dry_days>=10 & RH<40
    return out, d
m_va, _ = season_eval(va, 'val'); m_te, dte = season_eval(te, 'test')

tracker2 = OfflineEmissionsTracker(country_iso_code='IND', project_name='van-agni-infer',
                                   output_dir='outputs', output_file='codecarbon_infer.csv', log_level='error')
X = pd.concat([te[FEATURES]] * 10); tracker2.start(); t1 = time.time()
model.predict_proba(X); inf_s = time.time() - t1; inf_kg = tracker2.stop()
cc = pd.read_csv('outputs/codecarbon_train.csv').iloc[-1]; ci = pd.read_csv('outputs/codecarbon_infer.csv').iloc[-1]
imp = dict(zip(FEATURES, model.booster_.feature_importance('gain').round(1).tolist()))
metrics = {'validation_2024': m_va, 'test_2025': m_te, 'best_iteration': int(model.best_iteration_ or 400),
           'train_rows': int(len(tr)), 'train_seconds': round(train_s, 2),
           'train_kwh': float(cc.energy_consumed), 'train_kgco2e': float(cc.emissions),
           'infer_rows': int(len(X)), 'infer_seconds': round(inf_s, 3),
           'infer_kwh_per_1000': float(ci.energy_consumed) / len(X) * 1000,
           'infer_gco2e_per_1000': float(ci.emissions) * 1000 / len(X) * 1000,
           'feature_gain': dict(sorted(imp.items(), key=lambda kv: -kv[1]))}
json.dump(metrics, open('outputs/metrics.json', 'w'), indent=2)
joblib.dump(model, 'outputs/van_agni_lgbm.joblib')
print(json.dumps(metrics, indent=2))
