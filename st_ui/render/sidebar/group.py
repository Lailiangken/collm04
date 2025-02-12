import streamlit as st
from ...functions.sidebar import create_new_group, duplicate_group, delete_group, get_available_groups

def render_group_management(selected_group):
    with st.expander("グループ複製/追加/削除", expanded=True):
        render_group_duplication(selected_group)
        render_group_creation()
        render_group_deletion()
        st.markdown("defaultグループは削除できません。")

def render_group_duplication(selected_group):
    col1, col2 = st.columns([2, 1])
    with col1:
        duplicate_group_name = st.text_input(
            "複製先のグループ名", 
            key="duplicate_group_input",
            label_visibility="collapsed",
            placeholder="新しいグループ名を入力"
        )
    with col2:
        if st.button("グループを複製", key="duplicate_group"):
            if duplicate_group(selected_group, duplicate_group_name):
                st.success(f"グループ '{selected_group}' を複製し、'{duplicate_group_name}' として保存しました")
                st.rerun()
            else:
                st.error("グループの複製に失敗しました")

def render_group_creation():
    col1, col2 = st.columns([2, 1])
    with col1:
        new_group_name = st.text_input(
            "新規グループ名", 
            key="new_group_input",
            label_visibility="collapsed",
            placeholder="新規グループ名を入力"
        )
    with col2:
        if st.button("グループを追加", key="add_group"):
            if new_group_name:
                try:
                    create_new_group(new_group_name)
                    st.success(f"グループ '{new_group_name}' を作成しました")
                    st.rerun()
                except FileExistsError as e:
                    st.error(str(e))
            else:
                st.error("グループ名を入力してください")

def render_group_deletion():
    available_groups = get_available_groups()
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_delete_group = st.selectbox(
            "削除するグループを選択",
            available_groups,
            label_visibility="collapsed",
            index=available_groups.index("Agents") if "Agents" in available_groups else 0,
            placeholder="削除するグループを選択"
        )
    with col2:
        if selected_delete_group != "default":
            if st.button("グループを削除", key="delete_group"):
                if delete_group(selected_delete_group):
                    st.success(f"グループ '{selected_delete_group}' を削除しました")
                    st.rerun()
                else:
                    st.error("グループの削除に失敗しました")
        else:
            st.button("グループを削除", key="delete_group", disabled=True)
