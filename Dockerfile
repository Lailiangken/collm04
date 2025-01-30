FROM python:3.12-slim

# Dockerデーモン関連のパッケージをより確実にインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libyaml-dev \
    gcc \
    make \
    pkg-config \
    docker.io \
    docker-compose \
    curl \
    && rm -rf /var/lib/apt/lists/*




WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=Asia/Tokyo

EXPOSE 8502