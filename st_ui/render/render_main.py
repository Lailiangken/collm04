import streamlit as st
import logging
from .main.render_chat_settings import render_chat_section
from autogen_functions.group_chat.group_chat import GroupChatRunner
import asyncio
from pathlib import Path

def load_default_prompt(selected_group: str) -> str:
    prompt_path = Path(f"groups/{selected_group}/default_prompt.txt")
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""

def render_main_content(selected_group, selected_model):
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    
    st.title("Group Chat Assistant")
    st.markdown("グループチャットでは、SelectorGroupChatまたはMagenticOneGroupChatを選択できます。")
    
    st.info(f"現在選択中のグループ: {selected_group}")
    
    chat_type, use_web_surfer, use_code_executor = render_chat_section()
    
    default_prompt = load_default_prompt(selected_group)
    task = st.text_area(
        "議論するタスクや話題を入力してください:", 
        value=default_prompt,
        height=200,
        disabled=st.session_state.is_running
    )
    
    if st.session_state.is_running:
        st.write("処理中...")
        start_button = st.button("実行", disabled=True)
    else:
        start_button = st.button("実行")

    result_area = st.empty()
    
    with st.expander("チャットの進行状況", expanded=True):
        chat_area = st.empty()

    if start_button:
        st.session_state.is_running = True
        runner = GroupChatRunner()
        
        async def update_chat(message_stream):
            chat_area.markdown(message_stream)
            
        def update_result(result):
            result_area.markdown(f"### 最終結果:\n{result}")
        
        runner.message_callback = update_chat
        runner.result_callback = update_result
        
        try:
            results = asyncio.run(
                runner.stream_chat(
                    task=task,
                    chat_type=chat_type,
                    use_web_surfer=use_web_surfer,
                    use_code_executor=use_code_executor,
                    group_name=selected_group,
                    model_name=selected_model
                )
            )
            
            chat_info = {
                "chat_type": chat_type,
                "use_web_surfer": use_web_surfer,
                "use_code_executor": use_code_executor,
                "selected_group": selected_group,
                "task": task
            }
            
            return results['message_stream'], chat_info, results['last_result']
            
        finally:
            st.session_state.is_running = False
    return None, None, None