# Impact Data Sheet (Rule G1)
Measurement tool: CodeCarbon 3.3.2, OfflineEmissionsTracker, country IND. Raw output: outputs/codecarbon_train.csv, outputs/codecarbon_infer.csv.
Boundary: model training and scoring on our machine (CPU and RAM). Excludes data download, GitHub hosting and the reader's phone.

## Training
- Hardware: AMD Ryzen 7 9700X, 2 cores, no GPU, 3.8 GB RAM
- Runtime: 1.81 s
- Region: India
- Energy: 2.735e-05 kWh
- Grid intensity used: 713 gCO2e/kWh (CodeCarbon 3.3.2 built-in India mix, run date 3 Nov 2026)
- Emissions, all runs so far: 1.951e-05 kgCO2e per run (development used under 10 runs, so under 2e-4 kgCO2e)

## Inference
- Energy: 2.438e-08 kWh per 1,000 cell-scores
- Emissions: 1.739e-05 gCO2e per 1,000 cell-scores

## Water
- On-site cooling: 0 L (no data centre; PUE (Power Usage Effectiveness) 1.0, WUE (Water Usage Effectiveness) 0 as reported by CodeCarbon)
- Generation-side: energy × water intensity of India's grid. At an assumed 3.5 L/kWh for thermal-heavy generation, training uses about 9.6e-05 L. Assumption to be replaced by a sourced factor at Stage 3.
- Water stress context: Uttarakhand basins per WRI (World Resources Institute) Aqueduct, to be attached at Stage 3.

## SCI (Software Carbon Intensity, ISO/IEC 21031)
- Functional unit R: one daily risk map for Uttarakhand (113 cell-scores).
- SCI = (E × I + M) / R. Operational part: 2.75e-09 kWh × 713 g/kWh ≈ 1.97e-06 gCO2e per map. Embodied M is shared hardware, under 1 s of use per day.

## Baseline
- Manual alternative: range staff patrol historically worst areas. The model adds no measurable compute cost against that and improves catch rate from 20.4% to 33.2% (2025 test).
