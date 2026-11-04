# Van Agni | वन अग्नि
**7-day forest fire early warning for Indian forests. Uttarakhand pilot.**

Live demo: https://akshay-ira-2026.github.io/van-agni/

Van Agni scores every 0.25° grid cell (about 27 km) of Uttarakhand above 500 m elevation for the chance of a satellite-detected vegetation fire in the next 7 days, ranks the 10 cells to patrol first, and writes the alert in English and Hindi with the top reasons. It is advisory only: a forest officer verifies every alert before action.

## Why it matters
- India's Forest Survey of India (FSI) sends fire alerts *after* a fire is detected. Van Agni ranks where fire is *likely next week*, so beat staff, fire watchers and water/fire-line crews go there first.
- Uttarakhand loses thousands of hectares of chir pine forest every Feb-Jun season. 2021 and 2024 were severe years.

## How it works
1. **Fire history**: NASA FIRMS (Fire Information for Resource Management System) MODIS active-fire points, India archive 2019-2025, filtered to presumed vegetation fires (type 0).
2. **Weather**: NASA POWER daily (max temperature, humidity, max wind, rain) for training; Open-Meteo forecast API for the live run. No API keys.
3. **Terrain**: Open-Meteo elevation per cell.
4. **Features** (`src/features.py`): rain over 7/30/90 days, consecutive dry days, 7-day mean temperature and humidity, day of year, elevation, fire points in the cell last 7 days, the cell's historic fire rate (training years only, no leakage).
5. **Model** (`src/train.py`): LightGBM gradient-boosted trees. Train 2019-2023, validate 2024, test 2025.
6. **Alerts** (`src/alerts.py`): template text in English and Hindi with the top 3 reasons from the cell's own numbers. No language model at runtime, so nothing is invented.
7. **Dashboard** (`docs/index.html`): Leaflet map on GitHub Pages; a GitHub Action rescores live every day at 06:00 IST (Indian Standard Time).

## Results (held-out year 2025, never seen in training)
- ROC-AUC (area under the receiver operating curve): **0.914** (fire season Feb-Jun: 0.885)
- PR-AUC (precision-recall area): **0.296** against a base rate of 0.047
- Patrol the model's top 10 cells each day: catches **38.6%** of next-week fire cells, vs **20.4%** for the "historically worst 10 cells" baseline (+89%).
- Validation 2024: AUC 0.945, top-10 recall 31.2% vs 27.2%.
- Replay 22 Apr 2024: all 10 of the top 10 cells had real fires in the next 7 days.

## Measured footprint (CodeCarbon 3.3.2, offline, India grid)
- Training: 2.30e-04 kWh, 0.164 gCO2e, 4.6 s on 2 CPU cores, no GPU.
- Inference: 8.72e-08 kWh and 6.22e-05 gCO2e per 1,000 cell-scores.
- Raw logs: `outputs/codecarbon_train.csv`, `outputs/codecarbon_infer.csv`.

## Run it
```bash
pip install -r requirements.txt
python src/train.py                       # retrain + metrics + CodeCarbon logs
python src/predict.py live                # today's scores -> docs/live.json
python src/predict.py replay 2024-04-22   # score a past day and compare with real fires
pytest -q tests
```

## Limits (honest)
- MODIS sees fires about 1 km and larger, at satellite pass times. Small ground fires are missed, so the label undercounts.
- 27 km cells are coarse; the next step is 1 km cells with forest-cover, slope and road-distance layers and FSI beat boundaries.
- Weather in training (NASA POWER) and live (Open-Meteo) come from different sources.

## AI assistance disclosure (Rule G5)
Code, documents and data pipeline were written with Ira (an AI agent) under the team's direction. No generative model runs inside the product. See `submission/AI_DISCLOSURE.md`.

## Licence
Code MIT. Data: NASA FIRMS and NASA POWER (NASA open data), Open-Meteo (CC BY 4.0), OpenStreetMap tiles (ODbL).

## Deploy and reproduce
- Four ways to run it (free cloud, Docker, on-prem, edge/SMS): `deploy/DEPLOYMENT_OPTIONS.md`
- `docker build -t van-agni . && docker run -p 8000:8000 van-agni` then open http://localhost:8000
- Rebuild every number from raw data: `./reproduce.sh` (pinned versions in `requirements-lock.txt`)
- Security and compliance: `submission/SECURITY_COMPLIANCE.md` · Reproducibility: `submission/REPRODUCIBILITY.md`

## Pitch and money
- 8-minute pitch deck with speaker notes: `submission/PITCH_DECK.pptx`
- 5-year financial model: `submission/FINANCIAL_MODEL.xlsx`
- Stage 3 walkthrough script: `submission/WALKTHROUGH_SCRIPT.md`

- Screen recording of the demo (silent, narrate with WALKTHROUGH_SCRIPT.md): `submission/DEMO_RECORDING.mp4`
- Narrated walkthrough video with captions (Stage 3): `submission/WALKTHROUGH_VIDEO.mp4`

## Model v2 (4 Nov 2026): VIIRS 375 m satellite signal
- Added NASA VIIRS (Visible Infrared Imaging Radiometer Suite) S-NPP 375 m detections and fire radiative power: past 3 and 7 day counts, 7-day FRP (Fire Radiative Power), a vapour pressure deficit proxy and each cell's VIIRS fire history (training years only).
- All new inputs come from the public 7-day near-real-time feed, so the daily live job uses them too.
- 2025 held-out: AUC 0.914 (was 0.909), PR-AUC 0.296 (was 0.273), top-10 patrol recall 38.6% (was 33.2%) vs 20.4% baseline.
- Archive: data/firms_viirs_snpp_uttarakhand_2019_2025.csv.gz (116,060 detections, 2019-2025).
