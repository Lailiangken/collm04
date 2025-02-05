import streamlit as st
import json
import os
from pathlib import Path
from autogen_functions.group_chat.group_chat_043 import run_group_chat

def load_agent_configs():
    agent_dir = Path("autogen_functions/group_chat/agents")
    configs = {}
    for config_file in agent_dir.glob("*_config.json"):
        with open(config_file, "r") as f:
            configs[config_file.stem] = {
                "path": config_file,
                "data": json.load(f)
            }
    return configs

def save_agent_config(file_path, config):
    with open(file_path, "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def format_task_result(task_result):
    """Format the TaskResult object into Markdown."""
    md_output = "# 議論の結果\n\n"
    
    for message in task_result.messages:
        md_output += f"## {message.source.capitalize()}\n"
        md_output += f"{message.content}\n\n"
    
    return md_output

def main():
    st.title("Group Chat Assistant")

    # サイドバーにエージェント設定編集セクションを追加
    with st.sidebar:
        st.header("エージェント設定")
        
        # 全エージェントの設定を読み込み
        agent_configs = load_agent_configs()
        
        # タブでエージェントを切り替え
        agent_tabs = st.tabs(list(agent_configs.keys()))
        
        for tab, (agent_name, config_data) in zip(agent_tabs, agent_configs.items()):
            with tab:
                # 名前の編集
                new_name = st.text_input(
                    "Name", 
                    config_data["data"]["name"],
                    key=f"{agent_name}_name"
                )
                
                # システムメッセージの編集
                new_system_message = st.text_area(
                    "System Message", 
                    config_data["data"]["system_message"],
                    height=200,
                    key=f"{agent_name}_system_message"
                )
                
                # 設定の保存ボタン
                if st.button("設定を保存", key=f"{agent_name}_save"):
                    updated_config = {
                        "name": new_name,
                        "system_message": new_system_message
                    }
                    save_agent_config(config_data["path"], updated_config)
                    st.success(f"{agent_name}の設定を保存しました")

    # チャットモードの選択
    chat_mode = st.selectbox(
        "チャットモードを選択してください:",
        ["通常チャット", "コード実行チャット"]
    )

    task = st.text_area("議論するタスクや話題を入力してください:", height=200)

    if 'processing' not in st.session_state:
        st.session_state.processing = False

    button_text = "処理中..." if st.session_state.processing else "実行"
    if st.button(button_text, disabled=st.session_state.processing) and task:
        try:
            st.session_state.processing = True
            with st.spinner("処理中..."):
                task_result = run_group_chat(task, chat_mode=chat_mode)
                formatted_result = format_task_result(task_result)
                st.markdown(formatted_result, unsafe_allow_html=True)
            st.session_state.processing = False
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.session_state.processing = False

if __name__ == "__main__":
    main()
