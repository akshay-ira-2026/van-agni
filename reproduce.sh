#!/usr/bin/env bash
# Rebuild every number in the submission from the raw data in data/.
set -euo pipefail
python -m pip install -r requirements.txt
python src/train.py            # trains, back-tests 2024/2025, writes outputs/metrics.json + CodeCarbon CSVs
python src/predict.py replay 2024-04-22
python src/predict.py replay 2025-04-01
python src/predict.py live     # needs internet (Open-Meteo + NASA FIRMS)
python -m pytest -q tests
echo "done: compare outputs/metrics.json with submission/IMPACT_DATA_SHEET.md"
