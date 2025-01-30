import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

class ModernGroupChatFunction:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_client = OpenAIChatCompletionClient(model=model_name)
        
        # エージェントの作成
        self.planner = AssistantAgent(
            "planner",
            self.model_client,
            system_message="プロジェクトマネージャーとして、タスクの計画と調整を行います。"
        )
        
        self.developer = AssistantAgent(
            "developer",
            self.model_client,
            system_message="プログラマーとして、技術的な実装の詳細を提案します。"
        )
        
        self.reviewer = AssistantAgent(
            "reviewer",
            self.model_client,
            system_message="コードレビュアーとして、品質とベストプラクティスを確認します。"
        )
        
        self.user_proxy = UserProxyAgent("user_proxy")
        
        # 終了条件の設定
        self.termination = TextMentionTermination("終了")
        
        # チームの設定
        self.team = RoundRobinGroupChat(
            [self.planner, self.developer, self.reviewer, self.user_proxy],
            termination_condition=self.termination
        )

    async def start_discussion(self, task: str) -> str:
        """
        グループディスカッションを開始する非同期メソッド
        
        Args:
            task: 議論するタスクや話題
        Returns:
            str: 議論の結果
        """
        result = await self.team.run(task=task)
        return result

def run_group_chat(task: str) -> str:
    """
    グループチャットを実行するためのヘルパー関数
    
    Args:
        task: 議論するタスクや話題
    Returns:
        str: 議論の結果
    """
    chat = ModernGroupChatFunction()
    return asyncio.run(chat.start_discussion(task))
