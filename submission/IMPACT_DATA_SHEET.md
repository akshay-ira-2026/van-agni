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
- On-site cooling: 0 L (no data centre; PUE (Power Usage Effectiveness) 1.0, WUE (Water Usage Effectiveness) 0 as reported by CodeCarbon).
- Generation-side factor: 3.5 L/kWh. Source: MoEF&CC (Ministry of Environment, Forest and Climate Change) Environment (Protection) Amendment Rules, Dec 2015: specific water consumption cap of 3.5 m3/MWh (= 3.5 L/kWh) for thermal plants installed before 1 Jan 2017, 3.0 m3/MWh for later plants. Coal supplies about three quarters of India's electricity, so the pre-2017 cap is a conservative upper bound for the grid mix. Older plants without ash-water recirculation can reach 5-9 m3/MWh (Power Line, Nov 2021), so a sensitivity range of 3.0-9.0 L/kWh is reported.
- Result: training 2.735e-05 kWh x 3.5 L/kWh = 9.6e-05 L (range 8.2e-05 to 2.5e-04 L). Daily scoring for a year: about 1.0e-05 kWh, so about 3.5e-05 L a year.
- Water-stress context: WRI (World Resources Institute) "Parched Power" (Luo, Krishnan and Sen, 2018) finds 14 of India's 20 largest thermal utilities have faced water shortages and that most plants face more water competition by 2030. Van Agni's runtime water use is negligible against that. Its field benefit runs the other way: fewer and smaller fires protect the Himalayan catchments (Ganga and Yamuna headwaters in Uttarakhand) that feed those basins, since burned slopes lose soil and spring recharge.
- References: MoEF&CC notification S.O. 3305(E), 7 Dec 2015; WRI India working paper "Parched Power", 2018; IRENA (International Renewable Energy Agency) "Water use in India's power generation", 2018.

## SCI (Software Carbon Intensity, ISO/IEC 21031)
- Functional unit R: one daily risk map for Uttarakhand (113 cell-scores).
- SCI = (E × I + M) / R. Operational part: 2.75e-09 kWh × 713 g/kWh ≈ 1.97e-06 gCO2e per map. Embodied M is shared hardware, under 1 s of use per day.

## Baseline
- Manual alternative: range staff patrol historically worst areas. The model adds no measurable compute cost against that and improves catch rate from 20.4% to 33.2% (2025 test).
