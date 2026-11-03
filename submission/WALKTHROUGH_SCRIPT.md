# Stage 3: 5-minute walkthrough (screen recording + voice)

0:00-0:30 Problem. Uttarakhand chir pine forests burn Feb-Jun. FSI (Forest Survey of India) alerts say where fire is; Van Agni says where it is likely next week.
0:30-1:15 Live map. https://akshay-ira-2026.github.io/van-agni/ . 113 cells of ~27 km above 500 m. Colour = 7-day fire chance. Rescored 06:00 IST daily by GitHub Actions.
1:15-2:15 Replay 22 Apr 2024. Red = very high risk, outlines = fires actually seen next 7 days. Top-10 patrol list: 10 of 10 burned. Read alert #1 in English and Hindi with its reasons.
2:15-3:00 Held-out 2025. AUC (Area Under the Curve) 0.909; daily top 10 catches 33.2% of fire cells vs 20.4% for historical hotspots.
3:00-3:45 Code tour. src/features.py (rain 7/30/90 days, dry streak, humidity, heat, wind, elevation, past fires), src/train.py (LightGBM, year splits), tests/ (pytest passing), commit history.
3:45-4:30 Green AI (Artificial Intelligence). CodeCarbon: training 0.000027 kWh, 1,000 scores 0.000017 gCO2e. No LLM (Large Language Model) at runtime. Impact Data Sheet in submission/.
4:30-5:00 Deploy and next. Free cloud, Docker, on-prem, SMS (Short Message Service) edge. Pilot Feb-Jun 2027 in Nainital or Almora. Advisory only: officer decides.
