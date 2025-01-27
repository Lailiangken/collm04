import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def get_chat_response(config_path='config.json'):
    """
    OpenAI APIを使用してチャットレスポンスを取得する関数

    Args:
        config_path (str): 設定ファイルのパス

    Returns:
        str: ChatGPTからのレスポンス内容
    """
    # ルートディレクトリに `.env` ファイルが存在することを前提とする
    load_dotenv()

    # JSONファイルから設定を読み込む
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"設定ファイル '{config_path}' が見つかりません") from e

    # 環境変数からAPIキーを取得
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("環境変数 'OPENAI_API_KEY' が設定されていません")

    # OpenAIクライアントを初期化
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=config['model'],
        messages=config['messages']
    )

    if response.choices:
        return response.choices[0].message.content
    else:
        raise ValueError("APIからのレスポンスが空です")

# 使用例
if __name__ == "__main__":
    response_text = get_chat_response()
    print(response_text)