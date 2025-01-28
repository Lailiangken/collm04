import os
import json
from typing import Dict
from pathlib import Path
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
import inspect

# 必須パラメータの定義
REQUIRED_PARAMS = {
    'user_proxy': {'name', 'system_message', 'human_input_mode'},
    'assistant': {'name', 'system_message', 'human_input_mode'}
}

# 設定エラー用のカスタム例外クラス
class ConfigurationError(Exception):
    pass

class LLMBaseFunction:
    # 初期化: モデル設定とエージェントの読み込み
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.config_list = {
            "model": model_name,
            "api_key": os.environ["OPENAI_API_KEY"]
        }
        
        # 継承先のクラスのディレクトリからagentsフォルダを参照
        current_dir = os.path.dirname(os.path.abspath(inspect.getmodule(self).__file__))
        config_path = os.path.join(current_dir, 'agents/user_proxy_config.json')
        self.user_proxy = self._create_user_proxy(config_path)
        self.assistants = self._load_assistant_configs()

    # UserProxyAgentの作成: ユーザー代理として動作するエージェントを設定
    def _create_user_proxy(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self._validate_config(config, 'user_proxy')
        base_config = self._create_base_config(config)
        return UserProxyAgent(**base_config)

    def _load_assistant_configs(self):
        assistants = {}
        current_dir = os.path.dirname(os.path.abspath(inspect.getmodule(self).__file__))
        agents_dir = Path(os.path.join(current_dir, 'agents'))        
    
        for config_file in agents_dir.glob('*.json'):
            if config_file.stem != 'user_proxy_config':
                assistant = self._create_assistant(str(config_file))
                assistants[assistant.name] = assistant
        return assistants

    # Assistantの作成: AIアシスタントエージェントを設定
    def _create_assistant(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self._validate_config(config, 'assistant')
        base_config = self._create_base_config(config)
        return AssistantAgent(**base_config)

    # 基本設定の作成: エージェントの共通設定を生成
    def _create_base_config(self, config: Dict):
        base_config = {
            'name': config['name'],
            'system_message': config['system_message'],
            'human_input_mode': config['human_input_mode'],
            'max_consecutive_auto_reply': config.get('max_consecutive_auto_reply', 10),
            'llm_config': self.config_list
        }
        
        # オプション設定の追加
        if 'code_execution_config' in config:
            base_config['code_execution_config'] = config['code_execution_config']
        if 'description' in config:
            base_config['description'] = config['description']
        if 'function_map' in config:
            base_config['function_map'] = config['function_map']
        if 'is_termination_msg' in config:
            base_config['is_termination_msg'] = lambda x: isinstance(x, dict) and x.get('content', '').rstrip().endswith(config['is_termination_msg'])
            
        return base_config
    # アシスタント設定の読み込み: 複数のアシスタント設定を読み込む
    def _load_assistant_configs(self):
        assistants = {}
        current_dir = os.path.dirname(os.path.abspath(inspect.getmodule(self).__file__))
        agents_dir = Path(os.path.join(current_dir, 'agents'))        
        
        for config_file in agents_dir.glob('*.json'):
            if config_file.stem != 'user_proxy_config':
                assistant = self._create_assistant(str(config_file))
                assistants[assistant.name] = assistant
        return assistants

    # 設定の検証: 必須パラメータの存在確認
    def _validate_config(self, config: Dict, role_type: str):
        missing_params = REQUIRED_PARAMS[role_type] - set(config.keys())
        if missing_params:
            raise ConfigurationError(f"Missing required parameters for {role_type}: {missing_params}")

    # チャット履歴の取得: 会話履歴を返す
    def get_chat_history(self):
        return self.conversation_result.chat_history if hasattr(self, 'conversation_result') else []


