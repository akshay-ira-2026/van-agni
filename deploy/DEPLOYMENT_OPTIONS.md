# Deployment options

Van Agni is one small Python job plus a static web page. It runs the same way on four kinds of host.

## 1. Free cloud (live now)
- GitHub Actions runs `python src/predict.py live` at 06:00 IST (Indian Standard Time) every day.
- GitHub Pages serves `docs/` as the map: https://akshay-ira-2026.github.io/van-agni/
- Cost: zero. No server to patch.

## 2. Container (state data centre or any cloud VM (Virtual Machine))
```
docker build -t van-agni .
docker run -p 8000:8000 van-agni
```
- Scores today's risk on start, then serves the map at http://localhost:8000
- Schedule a daily restart (cron or Kubernetes CronJob) for fresh scores.
- Image is CPU-only, under 1 GB, no GPU (Graphics Processing Unit) needed.

## 3. On-premises server at a forest division office
```
pip install -r requirements.txt
crontab: 30 0 * * * cd /opt/van-agni && python src/predict.py live
python -m http.server 8000 --directory docs
```
- Works on a basic desktop. The model file is under 1 MB.

## 4. Edge / low connectivity
- The scored `docs/live.json` is about 20 KB. It can be pushed to field phones by SMS (Short Message Service) gateway or WhatsApp text: the top-10 alert lines are plain text in English and Hindi.
- If the internet fails, the container serves the last scores it has.

## Scaling to other states
- Change the bounding box and grid in `src/features.py`, rerun `reproduce.sh`. Training takes seconds on a CPU (Central Processing Unit).
