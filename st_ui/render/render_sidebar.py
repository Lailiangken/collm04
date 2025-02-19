import streamlit as st
from .sidebar.group import render_group_management
from .sidebar.agent import render_agent_settings
from .sidebar.logging import render_logging_section
from ..functions.sidebar import get_available_groups
from autogen_functions.load_model import list_available_models

def render_sidebar():
    with st.sidebar:
        # モデル選択セクション
        st.header("モデル設定")
        available_models = list_available_models()
        selected_model = st.selectbox(
            "使用するモデルを選択",
            available_models,
            index=available_models.index("azure_gpt4o_1") if "azure_gpt4o_1" in available_models else 0
        )

        # グループ設定セクション
        st.header("グループ設定")
        available_groups = get_available_groups()
        
        if not available_groups:
            st.warning("利用可能なグループがありません")
            return None, None
            
        selected_group = st.selectbox(
            "読み込むグループを選択",
            available_groups,
            index=available_groups.index("default") if "default" in available_groups else 0
        )

        render_group_management(selected_group)
        render_agent_settings(selected_group)
        
        return selected_group, selected_model