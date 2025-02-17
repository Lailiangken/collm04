import streamlit as st
from typing import Optional
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import AgentEvent, ChatMessage, ModelClientStreamingChunkEvent



class StreamlitConsoleHandler:
    def __init__(self, chat_area):
        self.chat_area = chat_area
        self.display_text = ""
        self.streaming_chunks = []


    async def handle_message(self, message):
        if isinstance(message, TaskResult):
            # TaskResultの場合は最後のメッセージを表示
            if message.messages:
                last_message = message.messages[-1]
                self.display_text += f"\n--- Final Result ---\n{last_message.content}\n"

        elif isinstance(message, ModelClientStreamingChunkEvent):
            self.streaming_chunks.append(message.content)
            self.display_text += message.content
        else:
            if self.streaming_chunks:
                self.streaming_chunks.clear()
                self.display_text += "\n"
            else:
                self.display_text += f"\n--- {message.source} ---\n{message.content}\n"
            


        # Streamlitの表示を更新
        self.chat_area.markdown(self.display_text)
