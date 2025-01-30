import asyncio
import os
import logging
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_functions.load_agents import load_agents_from_directory
from autogen_functions.load_model import load_model_from_config
from autogen_functions.logging_agents import LoggingAssistantAgent, LoggingUserProxyAgent

class GroupChatExample:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, "agents")
        
        # gpt-4o_1の設定を使用
        self.model_client = load_model_from_config("gpt-4o_1")
        self.agents = load_agents_from_directory(agents_dir, self.model_client, agent_class=LoggingAssistantAgent)
        
        self.user_proxy = LoggingUserProxyAgent(
            name="user_proxy",
            description="A user proxy that helps with the task."
        )
        
        self.termination = TextMentionTermination("TERMINATE")
        
        self.team = RoundRobinGroupChat(
            participants=self.agents + [self.user_proxy],
            termination_condition=self.termination
        )

    async def start_discussion(self, task: str) -> str:
        logging.info("チャットを開始します...")
        result = await self.team.run(task=task)
        logging.info("チャットが終了しました。")
        return result

def run_group_chat(task: str) -> str:
    chat = GroupChatExample()
    return asyncio.run(chat.start_discussion(task))
