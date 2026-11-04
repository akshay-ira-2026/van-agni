# Business case

## Who pays and who uses it
- Users: range officers, divisional forest officers (DFOs), beat guards, Van Panchayats and JFM (Joint Forest Management) committees.
- Buyers: state forest departments. Uttarakhand alone has about 38,000 sq km of forest and loses thousands of hectares a year to fire (FSI (Forest Survey of India) ISFR (India State of Forest Report) and FSI fire alert data).
- Funding routes that already exist: CAMPA (Compensatory Afforestation Fund Management and Planning Authority) state funds, the FFPM (Forest Fire Prevention and Management) scheme of MoEF&CC, SDRF (State Disaster Response Fund) mitigation windows, and CSR (Corporate Social Responsibility) grants for climate and biodiversity.

## Model: open core, paid service
- Code and model stay free and open (MIT licence). A state can self-host at zero licence cost.
- Revenue comes from what a department does not want to build itself:
  1. State setup: INR 8 lakh one-time (finer 1 km grid, local fire records, training range staff).
  2. Annual support: INR 3 lakh per state (seasonal retraining, helpdesk, accuracy report each season).
  3. SMS (Short Message Service) alerts to beat guards, billed at cost.
- Five-year plan (FINANCIAL_MODEL.xlsx): 1 state in 2027, 14 by 2031; break-even in year 1 on a part-time team; net INR 38 lakh in 2031.

## Why a department would buy it
- Costs less than one fire-watcher post per division per year.
- Measurable: every season ends with a report of alerts vs fires seen, so the department sees value in its own numbers.
- Runs on free hosting or its own desktop, so no new IT (Information Technology) procurement.

## Competition and edge
- FSI FAST alerts detect fires already burning; Van Agni predicts the next 7 days. They work together: FSI tells where fire is, Van Agni where to patrol first.
- Global tools (e.g. fire weather indices) are not tuned to Indian fire records or delivered in Hindi to beat guards.
- Edge: tiny compute footprint (0.000230 kWh to train), explainable alerts, offline and SMS delivery.

## Risks and answers
- Slow government buying: start with a pilot paid from existing FFPM or CSR money; publish results.
- Alert fatigue: only top 10 cells a day, each with reasons.
- Satellite gaps (cloud, small fires): add ground reports from beat guards as a second data source in year 2.

## Pilot
- Feb-Jun 2027 in Nainital or Almora divisions. Measure hectares burned and time to first response against neighbouring ranges.
