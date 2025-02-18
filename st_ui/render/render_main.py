import streamlit as st
import logging
from .main.render_chat import render_chat_section
from autogen_functions.group_chat.group_chat import GroupChatRunner
from ..utils.formatters import format_task_result
from .console_handler import StreamlitConsoleHandler
import asyncio

from autogen_functions.group_chat.group_chat import GroupChatExample

class StreamlitChatUI:
    def __init__(self, chat_area=None, result_area=None):
        self.chat_area = chat_area or st.empty()
        self.result_area = result_area or st.empty()
        self.console_handler = StreamlitConsoleHandler(self.chat_area)
    
    async def update_chat(self, message):
        await self.console_handler.handle_message(message)
    
    def update_result(self, result):
        self.result_area.markdown(f"### 最終結果:\n{result}")

def render_main_content(selected_group):
    st.title("Group Chat Assistant")
    st.markdown("グループチャットでは、SelectorGroupChatまたはMagenticOneGroupChatを選択できます。")
    
    st.info(f"現在選択中のグループ: {selected_group}")
    
    # 入力セクション
    chat_type, use_web_surfer, use_code_executor = render_chat_section()
    task = st.text_area("議論するタスクや話題を入力してください:", height=200)
    
    # 実行ボタンを入力欄の直後に配置
    start_button = st.button("実行")

    # 結果表示エリア
    result_area = st.empty()
    
    # チャット進行状況エリア
    with st.expander("チャットの進行状況", expanded=True):
        chat_area = st.empty()

    if start_button:
        ui = StreamlitChatUI(chat_area=chat_area, result_area=result_area)
        runner = GroupChatRunner()
        runner.set_callbacks(
            message_callback=ui.update_chat,
            result_callback=ui.update_result
        )
        
        messages, last_result = asyncio.run(
            runner.run_chat(
                task=task,
                chat_type=chat_type,
                use_web_surfer=use_web_surfer,
                use_code_executor=use_code_executor,
                group_name=selected_group
            )
        )

        chat_info = {
            "chat_type": chat_type,
            "use_web_surfer": use_web_surfer,
            "use_code_executor": use_code_executor,
            "selected_group": selected_group,
            "task": task
        }
        
        return ui.console_handler.display_text, chat_info, last_result
    
    return None, None, None   