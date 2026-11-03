import sys, json; sys.path.insert(0, 'src')
from alerts import alert, level
def test_levels():
    assert level(0.6)[0] == 'VERY HIGH' and level(0.3)[0] == 'HIGH' and level(0.12)[0] == 'MODERATE' and level(0.01)[0] == 'LOW'
def test_alert_bilingual_and_advisory():
    e, h = alert({'p': 0.7, 'lat': 29.1, 'lon': 79.9, 'dry_days': 20, 'rh7': 25, 'fires_past7': 3, 'T2M_MAX': 33, 'hist_rate': 0.1})
    assert 'Advisory only' in e and 'केवल सलाह' in h and 'VERY HIGH' in e
def test_alert_no_reasons_falls_back():
    e, h = alert({'p': 0.02, 'lat': 30, 'lon': 79, 'dry_days': 0, 'rh7': 80, 'fires_past7': 0, 'T2M_MAX': 10, 'hist_rate': 0})
    assert 'seasonal risk' in e
def test_metrics_beat_baseline():
    m = json.load(open('outputs/metrics.json'))['test_2025']
    assert m['auc'] > 0.85 and m['top10_recall'] > m['baseline_top10_recall_hist_only']
def test_replay_files_valid():
    for n in ['docs/replay_2024-04-22.json', 'docs/replay_2025-04-01.json', 'docs/live.json']:
        j = json.load(open(n)); assert len(j['top10']) == 10 and all(0 <= c['p'] <= 1 for c in j['cells'])
