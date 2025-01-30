import json
import os
from autogen_agentchat.agents import AssistantAgent

def load_agents_from_directory(agents_dir, model_client, agent_class=AssistantAgent):
    """
    指定されたディレクトリからエージェントを読み込む関数
    
    Args:
        agents_dir (str): エージェント設定ファイルが格納されたディレクトリのパス
        model_client: モデルクライアントのインスタンス
        agent_class: エージェントのクラス（デフォルトはAssistantAgent）

    Returns:
        list: 指定されたエージェントクラスのインスタンスのリスト
    """
    agents = []
    for filename in os.listdir(agents_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(agents_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                agent_info = json.load(f)
                agent = agent_class(
                    agent_info['name'],
                    model_client,
                    system_message=agent_info['system_message']
                )
                agents.append(agent)
    return agents