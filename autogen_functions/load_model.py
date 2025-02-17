import json
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient

def load_model_from_config(model_name: str) -> OpenAIChatCompletionClient:
    """
    モデル名を指定してモデルクライアントを読み込む関数
    
    Args:
        model_name (str): モデル設定ファイルの名前（拡張子なし）

    Returns:
        OpenAIChatCompletionClient: 設定されたモデルクライアントのインスタンス
    """
    # autogen_setting/models フォルダのパスを取得
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "autogen_setting", "models")
    config_path = os.path.join(models_dir, f"{model_name}.json")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Model config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        model_config = json.load(f)
    
    # APIキーの処理
    api_key = model_config.get("api_key")
    if api_key is None or api_key == "" or api_key.upper() == "ENV":
        api_key = os.environ.get("OPENAI_API_KEY")
    
    return OpenAIChatCompletionClient(
        model=model_config["model"],
        model_info={
            "vision": model_config.get("vision", False),
            "function_calling": model_config.get("function_calling", True),
            "json_output": model_config.get("json_output", True),
            "family": model_config.get("family", "GPT_4")
        },
        api_key=api_key,
        temperature=model_config.get("temperature", 0.7),
        max_tokens=model_config.get("max_tokens", 2000)
    )    