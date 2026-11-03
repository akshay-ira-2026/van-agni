# Reproducibility pack

1. `git clone https://github.com/akshay-ira-2026/van-agni && cd van-agni`
2. `./reproduce.sh` (or `docker build -t van-agni . && docker run -p 8000:8000 van-agni`)
3. Compare `outputs/metrics.json` with the numbers in IMPACT_DATA_SHEET.md and MODEL_CARD.md.

What is pinned
- Raw inputs are committed in `data/`: FIRMS MODIS (Moderate Resolution Imaging Spectroradiometer) points 2019-2025 for Uttarakhand, NASA POWER daily weather 2019-2025, the 113-cell grid with elevation.
- Splits are fixed by year: train 2019-2023, validate 2024, test 2025.
- LightGBM settings are in `src/train.py`; early stopping picked iteration 167.
- Raw CodeCarbon output: `outputs/codecarbon_train.csv`, `outputs/codecarbon_infer.csv`.
- Tests: `python -m pytest -q tests`.

Expected results (2025 test year): AUC (Area Under the Curve) 0.909, top-10 patrol recall 33.2% vs 20.4% for the historical-hotspot baseline. Small differences in the 3rd decimal can come from library versions.
