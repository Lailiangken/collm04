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

RUN groupmod -g 989 docker && \
    usermod -aG docker root


WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


RUN python /usr/local/lib/python3.12/site-packages/playwright install

RUN playwright install-deps

# Microsoft の署名キーを追加
RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor | \
    tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null

# Azure CLI のリポジトリを追加
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/azure-cli.list

# Azure CLI のインストール
RUN apt-get update && apt-get install -y azure-cli



ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=Asia/Tokyo

EXPOSE 8502
EXPOSE 8503