FROM python:3.12-slim

WORKDIR /app

# OSパッケージのセキュリティパッチ適用（S-02で検出したCritical/High計18件対応、ベースイメージ由来）
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=2", "--threads=4", "--access-logfile=-", "--error-logfile=-", "app:app"]
