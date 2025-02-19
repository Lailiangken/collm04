import streamlit as st
from st_ui.render.render_sidebar import render_sidebar
from st_ui.render.render_main import render_main_content
from st_ui.render.console_handler import StreamlitConsoleHandler
from autogen_functions.group_chat.group_chat import GroupChatExample
import os
from datetime import datetime
import json
import asyncio
from autogen_agentchat.base import TaskResult

class ChatRunner:
    def __init__(self, chat_area=None, result_area=None):
        self.chat_area = chat_area or st.empty()
        self.result_area = result_area or st.empty()
        self.console_handler = StreamlitConsoleHandler(self.chat_area)
    
    async def run_chat(self, chat_type: str, task: str):
        chat = GroupChatExample(chat_type=chat_type)
        stream = chat.team.run_stream(task=task)
        
        async for message in stream:
            if isinstance(message, TaskResult):
                if message.messages:
                    final_message = message.messages[-1]
                    self.result_area.markdown(f"### 最終結果:\n{final_message.content}")
            await self.console_handler.handle_message(message)
        
        chat_info = {
            "chat_type": chat_type,
            "task": task,
            "timestamp": datetime.now().isoformat()
        }
        return self.console_handler.display_text, chat_info, final_message.content

def save_result(formatted_result, chat_info, last_result):
    if formatted_result:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join('output', timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        result_path = os.path.join(output_dir, 'chat_history.md')
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        
        chatinfo_path = os.path.join(output_dir, 'chat_info.json')
        with open(chatinfo_path, 'w', encoding='utf-8') as f:
            json.dump(chat_info, f, ensure_ascii=False, indent=2)
        
        last_result_path = os.path.join(output_dir, 'last_result.md')
        with open(last_result_path, 'w', encoding='utf-8') as f:
            f.write(last_result)

        st.success(f"結果を保存しました: {result_path}")

def main():
    selected_group, selected_model = render_sidebar()  # selected_modelを受け取る
    if not selected_group:
        return
    
    formatted_result, chat_info, last_result = render_main_content(selected_group, selected_model)  # selected_modelを渡す
    if formatted_result:
        save_result(formatted_result, chat_info, last_result)

if __name__ == "__main__":
    main()   