import json
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

def list_available_models() -> list[str]:
    """
    利用可能なモデル名のリストを返す関数
    
    Returns:
        list[str]: 利用可能なモデル名のリスト（拡張子なし）
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "autogen_setting", "models")
    
    # .jsonファイルを検索してモデル名を抽出
    model_files = [f[:-5] for f in os.listdir(models_dir) if f.endswith('.json')]
    return model_files

def load_model_from_config(model_name: str):
    """
    モデル名を指定してモデルクライアントを読み込む関数
    
    Args:
        model_name (str): モデル設定ファイルの名前（拡張子なし）

    Returns:
        モデルクライアントのインスタンス
    """    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "autogen_setting", "models")
    config_path = os.path.join(models_dir, f"{model_name}.json")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Model config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        model_config = json.load(f)
    
    # Azure OpenAI モデルの設定
    if model_config.get("provider") == "azure":
        return AzureOpenAIChatCompletionClient(
            azure_endpoint=model_config["azure_endpoint"],
            azure_deployment=model_config["azure_deployment"],
            model=model_config["model"],
            api_version=model_config["api_version"],
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            model_info={
                "vision": model_config.get("vision", False),
                "function_calling": model_config.get("function_calling", True),
                "json_output": model_config.get("json_output", True),
                "family": model_config.get("family", "GPT_4")
            }
        )
    
    # OpenAI モデルの設定
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