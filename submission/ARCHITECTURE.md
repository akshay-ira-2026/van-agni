# Solution architecture: Van Agni

## Data flow
1. Ingest (daily, 06:00 IST, GitHub Actions): NASA FIRMS South Asia 7-day MODIS CSV (no key), Open-Meteo forecast with 92 past days (no key).
2. Grid: 0.25° cells over Uttarakhand, kept if elevation is 500 m or more (113 cells). Fire points snapped to cells.
3. Features (src/features.py): rolling rain 7/30/90 days, dry-day streak, 7-day temperature and humidity, day of year, elevation, fire points last 7 days, historic fire rate.
4. Score (src/predict.py): LightGBM, about 1 ms per 1,000 cells on one CPU core.
5. Publish: docs/live.json committed by the bot, served by GitHub Pages; Leaflet map reads it in the browser.
6. Alert (src/alerts.py): top 10 cells, English and Hindi text, top 3 reasons from the cell's own numbers.
7. Human: range officer verifies and dispatches. Nothing acts automatically.

## Why AI is needed
- Fire risk depends on several interacting signals (dryness built up over weeks, humidity, heat, recent fire nearby, terrain). A fixed rule like "dry for 10 days" ranks badly.
- On the held-out year 2025 the model's daily top-10 list caught 33.2% of next-week fire cells against 20.4% for patrolling the historically worst cells.
- A small tree model was chosen over deep learning: tabular data, explainable reasons, trains in seconds on a CPU.

## Stack, justified
- Python + pandas: standard, free, easy for forest-department analysts to read.
- LightGBM: best accuracy per watt for tabular data, no GPU.
- GitHub Actions + Pages: free, zero servers, static files cache well and load on 2G.
- Leaflet + OpenStreetMap: open, light (about 40 KB), works on low-end phones.

## Deployment options
- Cloud (default): GitHub Actions + Pages. Zero cost, no server to secure.
- On-premise: one Python cron job on a state forest department server (NIC (National Informatics Centre) cloud or a desktop), same code.
- Edge: model file is 0.6 MB; scoring can run on a Raspberry Pi class device at a range office with cached weather.
- Geo-distributed: one model per state or forest type, same pipeline, run in parallel.

## Scalability, security, performance
- All India at 0.25° is about 5,000 cells, at 1 km about 3 million cell-days a day: still minutes on one CPU.
- No personal data, no login, no write access from the public page. Repo secrets not needed (all APIs are keyless).
- Failure handling: if a source fails, the Action fails and yesterday's live.json stays up with its date shown.
