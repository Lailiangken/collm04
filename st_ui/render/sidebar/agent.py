import streamlit as st
from ...functions.agent_config import (
    create_new_agent_config,
    load_agent_configs,
    save_agent_config,
    delete_agent_config
)
from autogen_functions.tools_manager import ToolsManager

def render_agent_settings(selected_group):
    st.header("エージェント設定")
    st.markdown("defaultグループのエージェントは編集できません。")
    render_agent_creation(selected_group)
    # ToolsManagerのインスタンス化
    tools_manager = ToolsManager()
    available_tools = tools_manager.list_available_functions()
    
    agent_configs = load_agent_configs(selected_group)
    if agent_configs:
        render_existing_agents(selected_group, agent_configs, available_tools)
    else:
        st.info("このグループにはエージェントが存在しません。新しいエージェントを追加してください。")
    
    

def render_existing_agents(selected_group, agent_configs, available_tools):
    agent_tabs = st.tabs(list(agent_configs.keys()))
    for tab, (agent_name, config_data) in zip(agent_tabs, agent_configs.items()):
        with tab:
            new_name = st.text_input(
                "Name",
                config_data["data"]["name"],
                key=f"{agent_name}_name"
            )
            new_system_message = st.text_area(
                "System Message",
                config_data["data"]["system_message"],
                height=200,
                key=f"{agent_name}_system_message"
            )
            new_description = st.text_area(
                "Description",
                config_data["data"].get("description", ""),
                height=100,
                key=f"{agent_name}_description"
            )
            
            # ツール選択機能の追加
            selected_tools = st.multiselect(
                "Select Tools",
                available_tools,
                default=config_data["data"].get("tools", []),
                key=f"{agent_name}_tools"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("設定を保存", key=f"{agent_name}_save", disabled=selected_group=="default"):
                    updated_config = {
                        "name": new_name,
                        "system_message": new_system_message,
                        "description": new_description,
                        "tools": selected_tools  # ツール設定を追加
                    }
                    save_agent_config(config_data["path"], updated_config)
                    st.success(f"{agent_name}の設定を保存しました")
            with col2:
                if st.button("Agentを削除", key=f"{agent_name}_delete", disabled=selected_group=="default"):
                    if delete_agent_config(config_data["path"]):
                        st.success(f"{agent_name}を削除しました")
                        st.rerun()
                    else:
                        st.error("削除に失敗しました")

def render_agent_creation(selected_group):
    with st.expander("エージェント追加", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            new_agent_name = st.text_input(
                "新規エージェント名",
                key="new_agent_input",
                label_visibility="collapsed",
                placeholder="エージェント名を入力"
            )
        with col2:
            if st.button("Agentを追加", key="add_agent", disabled=selected_group=="default"):
                if new_agent_name:
                    try:
                        create_new_agent_config(new_agent_name, selected_group)
                        st.success(f"エージェント '{new_agent_name}' を作成しました")
                        st.rerun()
                    except FileExistsError as e:
                        st.error(str(e))
                else:
                    st.error("エージェント名を入力してください")