# Van Agni: run the daily scoring and serve the map, offline-capable
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# score today's risk, then serve docs/ (map + json) on port 8000
CMD ["sh", "-c", "python src/predict.py live || echo 'live fetch failed, serving last scores'; python -m http.server 8000 --directory docs"]
