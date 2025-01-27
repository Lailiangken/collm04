from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import autogen
from pathlib import Path
import json
import os

class LLMFunction:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.config_list = [
            {
                "model": model_name,
                "api_key": os.environ["OPENAI_API_KEY"]
            }
        ]
        
        self.assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config={"config_list": self.config_list},
            system_message="You are a helpful AI assistant."
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "coding"},
            llm_config={"config_list": self.config_list},
        )
        
    def __call__(self, user_input: str) -> str:
        self.user_proxy.initiate_chat(
            self.assistant,
            message=user_input
        )
        
        return "Chat completed"

def main():
    llm_func = LLMFunction()
    result = llm_func("Write a Python function to calculate fibonacci numbers")
    print(result)

if __name__ == "__main__":
    main()
