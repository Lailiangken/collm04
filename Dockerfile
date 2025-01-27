FROM python:3.12-slim

# システムパッケージの更新
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        git \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python パッケージの更新
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# 環境変数の設定
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=Asia/Tokyo

# Streamlitのポート設定
EXPOSE 8501


