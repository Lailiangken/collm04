import streamlit as st
from st_ui.render.console_handler import StreamlitConsoleHandler
from autogen_functions.group_chat.group_chat_mutli import GroupChatExample
import asyncio
from autogen_agentchat.base import TaskResult

class ChatRunner:
    def __init__(self, chat_area=None, result_area=None):
        self.chat_area = chat_area or st.empty()
        self.result_area = result_area or st.empty()
        self.console_handler = StreamlitConsoleHandler(self.chat_area)
    
    async def run_chat(self, task: str = "Hello World", chat_type: str = "magentic"):
        chat = GroupChatExample(chat_type=chat_type)
        stream = chat.team.run_stream(task=task)
        
        async for message in stream:
            if isinstance(message, TaskResult):
                # TaskResultの場合は上部の結果エリアに表示
                if message.messages:
                    final_message = message.messages[-1]
                    self.result_area.markdown(f"### 最終結果:\n{final_message.content}")
            await self.console_handler.handle_message(message)
        
        return self.console_handler.display_text

def main():
    st.title("AutoGen Chat Demo")
    
    # 結果表示エリアを先に確保

    
    chat_type = st.selectbox(
        "チャットタイプを選択",
        ["magentic", "selector"]
    )
    
    task = st.text_area("タスクを入力してください:", "Hello World")
    
    if st.button("実行"):
        chat_area = st.empty()
        result_area = st.empty()
        runner = ChatRunner(chat_area=chat_area, result_area=result_area)
        result = asyncio.run(runner.run_chat(task=task, chat_type=chat_type))

if __name__ == "__main__":
    main()