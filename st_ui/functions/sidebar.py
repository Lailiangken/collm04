import streamlit as st
from pathlib import Path
import logging
import json
import shutil
from .agent_config import (
    create_new_agent_config,
    load_agent_configs,
    save_agent_config,
    delete_agent_config
)

def get_available_groups():
    group_dir = Path("groups")
    return [d.name for d in group_dir.iterdir() 
            if d.is_dir() 
            and d.name != "template" 
            and not d.name.startswith("__")]

def create_new_group(group_name):
    template_dir = Path("template/agents")
    new_group_dir = Path("groups") / group_name / "agents"
    
    if new_group_dir.exists():
        raise FileExistsError(f"グループ '{group_name}' は既に存在します")
    
    new_group_dir.parent.mkdir(exist_ok=True)
    shutil.copytree(template_dir, new_group_dir)
    return new_group_dir

def duplicate_group(source_group_name, new_group_name):
    source_group_dir = Path("groups") / source_group_name
    new_group_dir = Path("groups") / new_group_name

    if not source_group_dir.exists():
        raise FileNotFoundError(f"ソースグループ '{source_group_name}' が存在しません")
    
    if new_group_dir.exists():
        raise FileExistsError(f"グループ '{new_group_name}' は既に存在します")

    shutil.copytree(source_group_dir, new_group_dir)
    return True

def delete_group(group_name):
    group_dir = Path("groups") / group_name
    if not group_dir.exists():
        return False
    shutil.rmtree(group_dir)
    return True


