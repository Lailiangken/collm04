# Group Chat Assistant

このプロジェクトは、Autogen(0.4.*)を利用したPythonコード作成補助用のグループチャットアシスタントを提供します。  
Streamlitを使用したWebインターフェースで、通常チャットとコード実行チャットの2つのモードを提供します。  
作者はこれをWSL2環境で開発しているので、他の環境での動作は確認していません。

## 機能

**通常チャット**: 複数のAIエージェントによる対話型チャット  
**コード実行チャット**: Pythonコードの生成と実行が可能なチャット  
## 必要条件

Docker  
Docker Compose  
OpenAI API Key  
## インストール

**リポジトリをクローン**: プロジェクトのリポジトリをローカルマシンにクローンします。

```bash git clone https://github.com/yourusername/collm04.git cd collm04 ```

**環境変数の設定**: プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を設定します。WORK_DIR はホストマシン上の作業ディレクトリを指定し、OPENAI_API_KEY にはOpenAIのAPIキーを設定してください。

``` WORK_DIR="/path/to/your/workspace" OPENAI_API_KEY="your-api-key" ```

**Dockerイメージのビルド**: Docker Composeを使用して、必要なDockerイメージをビルドします。

```bash docker-compose build ```

## 使用方法

**アプリケーションの起動**: Docker Composeを使用してアプリケーションを起動します。これにより、必要なコンテナが立ち上がり、アプリケーションが実行されます。

```bash docker-compose up ```

-d オプションを付けると、バックグラウンドでコンテナを実行できます。
**アプリケーションへのアクセス**: ブラウザで以下のURLにアクセスして、Streamlitのインターフェースを使用します。

``` http://localhost:8502 ```

**インターフェースの使用**:

チャットモードを選択（通常チャット/コード実行チャット）  
タスクや質問を入力  
"実行"ボタンをクリック  
**アプリケーションの停止**: アプリケーションを停止するには、以下のコマンドを使用します。

```bash docker-compose down ```

## プロジェクト構成

``` 
collm04/ 
├── autogen_functions/ 
│ └── group_chat/ 
│     └──agents/
│     │   └── (各エージェント情報).json
│     └── group_chat_043.py 
├── autogen_setting/
│ └── models/
│     └── gpt-4o_1.json
├── group_chat_app.py 
├── Dockerfile 
├── docker-compose.yml 
├── requirements.txt 
└── .env 
```

## 主要コンポーネント

`group_chat_app.py`: Streamlitベースのメインアプリケーション  
`group_chat_043.py`: グループチャットのコア機能  
`Dockerfile`: アプリケーションのコンテナ化設定  
`docker-compose.yml`: マルチコンテナ設定  

Docker周りについては作者もだいぶ苦戦したので、うまく動作しなければ教えてください。

## 実行例
[Sample](sample.pdf)  
サンプルを見ればわかる通り、コード実行チャットにおいてはだいぶ無駄な会話が多いです。Agentを追加、編集したりすることで効率化ができると思います。  
[動画](動作.pdf)  
サイズの制限で途中からですが、(デコードされてない文字列が)Logとして流れる様子を見ることができます。