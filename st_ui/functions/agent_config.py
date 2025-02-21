from pathlib import Path
import json

def create_new_agent_config(agent_name, group_name):
    config_path = Path("groups") / group_name / "agents" / f"{agent_name}_config.json"
    if config_path.exists():
        raise FileExistsError(f"エージェント '{agent_name}' は既に存在します")
    
    default_config = {
        "name": agent_name,
        "system_message": "新しいエージェントのシステムメッセージをここに入力してください",
        "description": "エージェントの説明をここに入力してください"
    }
    
    save_agent_config(config_path, default_config)
    return config_path

def load_agent_configs(group_name):
    agent_dir = Path("groups") / group_name / "agents"
    configs = {}
    for config_file in agent_dir.glob("*_config.json"):
        with open(config_file, "r", encoding="utf-8") as f:
            configs[config_file.stem] = {
                "path": config_file,
                "data": json.load(f)
            }
    return configs

def save_agent_config(file_path, config):
    with open(file_path, "w",encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def delete_agent_config(file_path):
    path = Path(file_path)
    if path.exists():
        path.unlink()
        return True
    return False
