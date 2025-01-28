# COLLM - Code Assistant
以下は自動生成で作成しています

コードレビューとコード生成を支援するAIアシスタントツール

## 環境構築

### 必要条件
- Python 3.9以上
- Docker
- OpenAI API Key
（製作者はWSL環境で作成しているので、以降の手順はWSL環境での作業を想定しています）

### Dockerを使った起動方法

## 1. Dockerのインストール

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo apt install docker-compose


## 2. 環境変数の設定

### .envファイルの作成
プロジェクトルートに`.env`ファイルを作成し、以下の内容を設定します:
OPENAI_API_KEY=your_api_key

あるいは、以下のコマンドを実行して環境変数を設定します:
export OPENAI_API_KEY=your_api_key


## 3. アプリケーションの起動

### Dockerイメージのビルド
```bash
docker-compose build --no-cache

### Dockerコンテナの起動
docker-compose up

### Dockerコンテナの停止
docker-compose down
```

## 4. アプリケーションの使用方法

### Webインターフェースへのアクセス
- ブラウザで http://localhost:8501 を開く
- Streamlitベースの直感的なUIが表示されます

### 基本機能
1. コードレビュー
   - Pythonコードを入力
   - AIによる詳細なレビューと改善提案を取得
   - 結果はMarkdown形式で表示

2. コード生成
   - 要件を自然言語で入力
   - AIが要件に基づいてPythonコードを生成
   - 生成されたコードはシンタックスハイライト付きで表示

### 出力管理
- すべての結果は`output`ディレクトリに自動保存
- ディレクトリ構造:
collm/ 
├── app.py # Streamlitメインアプリケーション 
├── code_review.py # コードレビュー機能 
├── get_chat_response.py # OpenAI API通信 
├── autogen_functions/ # 自動生成機能 
│ └── factory.py # 機能生成ファクトリー 
│ ├── docker/ # Docker関連 
│ ├── Dockerfile # Dockerイメージ定義 
│ └── docker-compose.yml # Docker環境設定 
│ ├── requirements.txt # 依存パッケージ一覧 
├── .env # 環境変数設定 
├── .gitignore # Git除外設定 
├── README.md # プロジェクト説明 
│ └── output/ # 生成結果の出力先 
├── code_review/ # レビュー結果 
│ └── YYYYMMDD_HHMMSS_query/ 
│ ├── generated_result.md 
│ ├── query.txt 
│ └── conversation.txt 
│ └── code_generator/ # コード生成結果 
└── YYYYMMDD_HHMMSS_query/ 
├── generated_result.py 
├── query.txt 
└── conversation.txt

### 高度な使用方法
- APIキーの動的変更が可能
- 生成結果の履歴管理
- 会話ログの保存と参照