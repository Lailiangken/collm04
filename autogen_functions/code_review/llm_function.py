import os
import json
from typing import Dict
from pathlib import Path
from autogen import UserProxyAgent, AssistantAgent
REQUIRED_PARAMS = {
    'user_proxy': {'name', 'system_message', 'human_input_mode'},
    'assistant': {'name', 'system_message', 'human_input_mode'}
}

class ConfigurationError(Exception):
    pass

class CodeReviewFunction:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.config_list = {
            "model": model_name,
            "api_key": os.environ["OPENAI_API_KEY"]
        }        
        # 現在のファイルからの相対パスを計算
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # UserProxyAgentの設定を読み込む
        config_path = os.path.join(current_dir, 'agents/user_proxy_config.json')
        self.user_proxy = self._create_user_proxy(config_path)
        
        # Assistantの設定を読み込む
        self.assistants = self._load_assistant_configs()
        
    def _create_user_proxy(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        self._validate_config(config, 'user_proxy')
        
        base_config = {
            'name': config['name'],
            'system_message': config['system_message'],
            'human_input_mode': config['human_input_mode'],
            'max_consecutive_auto_reply': config.get('max_consecutive_auto_reply', 10),
            'llm_config': self.config_list
        }
        
        if 'code_execution_config' in config:
            base_config['code_execution_config'] = config['code_execution_config']
        if 'is_termination_msg' in config:
            base_config['is_termination_msg'] = lambda x: x.get('content', '').rstrip().endswith(config['is_termination_msg'])
            
        return UserProxyAgent(**base_config)
    def _create_assistant(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        self._validate_config(config, 'assistant')
        
        base_config = {
            'name': config['name'],
            'system_message': config['system_message'],
            'human_input_mode': config['human_input_mode'],
            'max_consecutive_auto_reply': config.get('max_consecutive_auto_reply', 10),
            'llm_config': self.config_list
        }
        
        if 'description' in config:
            base_config['description'] = config['description']
        if 'function_map' in config:
            base_config['function_map'] = config['function_map']
            
        return AssistantAgent(**base_config)
        
    def _load_assistant_configs(self):
        assistants = {}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = Path(os.path.join(current_dir, 'agents'))
        
        for config_file in agents_dir.glob('*.json'):
            if config_file.stem != 'user_proxy_config':
                assistant = self._create_assistant(str(config_file))
                assistants[assistant.name] = assistant
                
        return assistants    
    def _validate_config(self, config: Dict, role_type: str):
        missing_params = REQUIRED_PARAMS[role_type] - set(config.keys())
        if missing_params:
            raise ConfigurationError(f"Missing required parameters for {role_type}: {missing_params}")
    def __call__(self, code: str) -> str:
        # レビュー依頼と結果取得
        review_result = self.user_proxy.initiate_chat(
            self.assistants['code_reviewer'],
            message=f"このコードをレビューしてください:\n{code}",
            clear_history=True
        )
        
        # レビュー結果を取得
        review_content = review_result.chat_history[-1]['content']
        
        # 改善提案依頼と結果取得
        improvement_result = self.user_proxy.initiate_chat(
            self.assistants['code_improver'],
            message=f"以下のレビュー結果に基づいて、具体的な改善案を提示し、具体的なコードを挙げててください:\n\n{review_content}",
            clear_history=True
        )
        
        improvement_content = improvement_result.chat_history[-1]['content']
        
        return f"""
レビュー結果:
{review_content}

改善提案:
{improvement_content}
"""