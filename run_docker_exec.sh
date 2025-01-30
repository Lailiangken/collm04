#!/bin/bash

# 起動中のコンテナ名を取得
CONTAINER_NAME=$(docker ps --filter "ancestor=[イメージ名]" --format "{{.Names}}" | head -n 1)

# コンテナが見つからない場合のエラーハンドリング
if [ -z "$CONTAINER_NAME" ]; then
  echo "コンテナが見つかりません。"
  exit 1
fi

# コンテナに接続
docker exec -it "$CONTAINER_NAME" bash
