import asyncio
import os
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_functions.load_agents import load_agents_from_directory

class GroupChatExample:
    def __init__(self, model_name: str = "gpt-4"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, "agents")
        
        self.model_client = OpenAIChatCompletionClient(model=model_name)
        self.agents = load_agents_from_directory(agents_dir, self.model_client)
        
        # UserProxyAgentの設定を0.4仕様に更新
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            description="A user proxy that helps with the task.",
            verbose=True
        )
        
        self.termination = TextMentionTermination("!!TERMINATE!!")
        
        self.team = RoundRobinGroupChat(
            participants=self.agents + [self.user_proxy],
            termination_condition=self.termination
        )

    async def start_discussion(self, task: str) -> str:
        print("チャットを開始します...")
        result = await self.team.run(task=task)
        print("チャットが終了しました。")
        return result

def run_group_chat(task: str) -> str:
    chat = GroupChatExample()
    return asyncio.run(chat.start_discussion(task))
