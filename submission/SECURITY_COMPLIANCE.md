# Security and compliance summary

## Data
- Only public, open data: NASA FIRMS (Fire Information for Resource Management System) fire points, NASA POWER weather, Open-Meteo forecast and elevation.
- No personal data is collected, stored or processed. No user accounts.
- Licences: FIRMS and POWER are NASA open data; Open-Meteo data is CC BY 4.0, credited on the map.

## Code and supply chain
- Open source, MIT licence. Every change is in the public commit history.
- Dependencies are well-known packages (numpy, pandas, scikit-learn, lightgbm, requests, codecarbon) listed in requirements.txt.
- The daily job has write access only to this repository, and only commits `docs/live.json`.
- No API (Application Programming Interface) keys or secrets are needed to run it.

## Safety of outputs
- Every alert says "Advisory only: verify with beat staff". A forest officer decides every action.
- Alerts are filled-in templates from the model's own numbers. No language model writes them, so they cannot invent facts.
- Known failure: satellite fire records miss small or cloud-covered fires, so risk may be under-stated in cloudy weeks. This is stated on the model card.

## Indian rules it is built to fit
- DPDP (Digital Personal Data Protection) Act 2023: not triggered, since no personal data is processed.
- IT (Information Technology) Act 2000 and CERT-In (Indian Computer Emergency Response Team) directions: static site, no user data; incidents would be logged through the host.
- Data stays exportable as plain CSV (Comma-Separated Values) and JSON (JavaScript Object Notation) for any state data centre under the National Data Sharing and Accessibility Policy.
