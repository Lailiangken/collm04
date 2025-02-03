import asyncio
import os
import logging
import tempfile
from pathlib import Path
from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.teams import GroupChatManager
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent, LoggingAssistantAgent, LoggingUserProxyAgent
from autogen_functions.load_model import load_model_from_config
from autogen_agentchat.subscriptions import TypeSubscription

class GroupChatExample:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.work_dir = Path(tempfile.mkdtemp())
        self.work_dir.mkdir(exist_ok=True)
        self.runtime = SingleThreadedAgentRuntime()
        self.model_client = load_model_from_config("gpt-4o_1")
        
        # トピックタイプの定義
        self.coder_topic_type = "Coder"
        self.reviewer_topic_type = "Reviewer"
        self.user_topic_type = "User"
        self.executor_topic_type = "Executor"
        self.group_chat_topic_type = "group_chat"

        # エージェントの説明
        self.coder_description = "A coder who implements solutions in Python"
        self.reviewer_description = "A reviewer who checks and improves code quality"
        self.user_description = "A user proxy that helps with the task"
        self.executor_description = "An executor that runs code snippets"
        
        # コードエグゼキューターの初期化（非同期コンテキスト外での生成は可能）
        self.code_executor = DockerCommandLineCodeExecutor(
            work_dir=str(self.work_dir),
            image="python:3-slim",
            timeout=300
        )
    
    async def async_init(self):
        # CodeExecutorAgentの登録
        self.executor_agent_type = await CodeExecutorAgent.register(
            self.runtime,
            self.executor_topic_type,
            lambda: CodeExecutorAgent(
                name="executor",
                code_executor=self.code_executor
            )
        )
        
        # coder, reviewer, userエージェントの登録
        self.coder_agent_type = await LoggingAssistantAgent.register(
            self.runtime,
            self.coder_topic_type,
            lambda: LoggingAssistantAgent(
                name="coder",
                description=self.coder_description,
                model_client=self.model_client
            )
        )
        self.reviewer_agent_type = await LoggingAssistantAgent.register(
            self.runtime,
            self.reviewer_topic_type,
            lambda: LoggingAssistantAgent(
                name="reviewer",
                description=self.reviewer_description,
                model_client=self.model_client
            )
        )
        self.user_agent_type = await LoggingUserProxyAgent.register(
            self.runtime,
            self.user_topic_type,
            lambda: LoggingUserProxyAgent(
                name="user_proxy",
                description=self.user_description
            )
        )
        
        # サブスクリプションの追加
        for agent in [self.coder_agent_type, self.reviewer_agent_type, self.user_agent_type, self.executor_agent_type]:
            await self.runtime.add_subscription(
                TypeSubscription(topic_type=agent.type, agent_type=agent.type)
            )
            await self.runtime.add_subscription(
                TypeSubscription(topic_type=self.group_chat_topic_type, agent_type=agent.type)
            )
        
        # GroupChatManagerの登録
        self.group_chat_manager_type = await GroupChatManager.register(
            self.runtime,
            "group_chat_manager",
            lambda: GroupChatManager(
                participant_topic_types=[
                    self.coder_topic_type,
                    self.reviewer_topic_type,
                    self.user_topic_type,
                    self.executor_topic_type
                ],
                model_client=self.model_client,
                participant_descriptions=[
                    self.coder_description,
                    self.reviewer_description,
                    self.user_description,
                    self.executor_description
                ]
            )
        )
        await self.runtime.add_subscription(
            TypeSubscription(topic_type=self.group_chat_topic_type, agent_type=self.group_chat_manager_type.type)
        )

    @classmethod
    async def create(cls) -> "GroupChatExample":
        instance = cls()
        await instance.async_init()
        return instance

    async def start_discussion(self, task: str) -> str:
        logging.info("チャットを開始します...")
        self.runtime.start()
        try:
            async with self.code_executor:
                # GroupChatManagerのrunメソッドを非同期に呼び出す
                result = await self.group_chat_manager_type.run(task=task)
                await self.runtime.stop_when_idle()
                return result
        except Exception as e:
            logging.error(f"エラーが発生しました: {str(e)}")
            raise
        finally:
            await self.code_executor.stop()

def run_group_chat(task: str) -> str:
    async def main():
        chat = await GroupChatExample.create()
        return await chat.start_discussion(task)
    return asyncio.run(main())
