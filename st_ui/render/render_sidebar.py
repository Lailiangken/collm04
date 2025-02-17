import streamlit as st
from .sidebar.group import render_group_management
from .sidebar.agent import render_agent_settings
from .sidebar.logging import render_logging_section
from ..functions.sidebar import get_available_groups

def render_sidebar():
    with st.sidebar:
        st.header("グループ設定")
        available_groups = get_available_groups()
        
        if not available_groups:
            st.warning("利用可能なグループがありません")
            return None
            
        selected_group = st.selectbox(
            "読み込むグループを選択",
            available_groups,
            index=available_groups.index("default") if "default" in available_groups else 0
        )

        render_group_management(selected_group)
        render_agent_settings(selected_group)
        #render_logging_section()
        
        return selected_group
