# Green-AI implementation plan
- Small model by design: gradient-boosted trees, early stopping (best iteration 167 of 400).
- CPU only, no GPU, no language model at runtime (alerts are templates).
- Measured with CodeCarbon 3.3.2 on every training and inference run; raw CSVs in outputs/.
- Retrain once a year before the fire season, not daily.
- Run the daily score at 06:00 IST; static output served from CDN cache, so each map view costs almost nothing extra.
- Data kept small: 0.25° grid, gzip weather; repo under 10 MB.
- Next step for scale: 1 km grid only inside forest-cover mask, so cells outside forest are never scored.
