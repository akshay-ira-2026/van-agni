# Van Agni: 2-3 minute demo script

**0:00-0:20 | The problem**
"Every February to June, Uttarakhand's chir pine forests burn. Today the Forest Survey of India alert tells a range officer where a fire *is*. Van Agni tells them where fire is *likely next week*, so the patrol is already there."

**0:20-0:50 | Open the live map** (https://akshay-ira-2026.github.io/van-agni/)
"Each square is about 27 km. Colour is the chance of a fire in the next 7 days. It is November, off-season, so everything is green. The map rescores itself at 6 every morning from NASA fire data and the weather forecast."

**0:50-1:40 | Replay 22 April 2024**
Pick "Replay 22 Apr 2024" in the drop-down.
"This is peak season last year. Red squares are very high risk. The blue outlines are where fires were actually seen in the following week. The panel on the right is the patrol list: all 10 of the top 10 squares burned in the next 7 days."
Click the top alert. "Every alert gives its reasons in plain words, in English and Hindi: no rain for 49 days, humidity 24%, 44 fire points nearby this week."

**1:40-2:10 | Does it really work?**
Pick "Replay 1 Apr 2025".
"2025 was kept aside and never used in training. On it the model scores an AUC of 0.91, and a daily top-10 patrol list catches a third more fire cells than just patrolling the historically worst areas."

**2:10-2:40 | Green by design**
"The whole model trained in under 2 seconds on a laptop-class CPU: about 0.00003 kilowatt-hours, measured with CodeCarbon. Scoring all of Uttarakhand costs less energy than a phone screen for a second. No GPU, no language model at runtime."

**2:40-3:00 | Next**
"Next: 1 km cells with forest cover and slope, FSI beat boundaries, and SMS to beat guards. It is advisory only: the officer always decides."
