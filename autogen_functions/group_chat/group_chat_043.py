import asyncio
import os
import logging
import tempfile
from pathlib import Path
from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_functions.load_agents import load_agents_from_directory
from autogen_functions.load_model import load_model_from_config
from autogen_functions.logging_agents import LoggingAssistantAgent, LoggingUserProxyAgent
from autogen_functions.code_executor.executor_agent import ExecutorAgent

class GroupChatExample:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, "agents")
        # 一時ディレクトリをPathオブジェクトとして作成
        self.work_dir = Path(tempfile.mkdtemp())
        self.work_dir.mkdir(exist_ok=True)
        
        self.runtime = SingleThreadedAgentRuntime()
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
        self.runtime.start()
        
        # DockerCommandLineCodeExecutorの設定を改善
        executor = DockerCommandLineCodeExecutor(
            image="python:3-slim",
            work_dir=self.work_dir,
            timeout=300,  # タイムアウトを5分に設定
            auto_remove=True,
            stop_container=True
        )
        
        await ExecutorAgent.register(
            self.runtime,
            "executor",
            lambda: ExecutorAgent("Code executor agent", executor)
        )
        
        try:
            async with executor:
                result = await self.team.run(task=task)
                await self.runtime.stop_when_idle()
        except Exception as e:
            logging.error(f"エラーが発生しました: {str(e)}")
            raise
        finally:
            await executor.stop()
        
        logging.info("チャットが終了しました。")
        return result

def run_group_chat(task: str) -> str:
    chat = GroupChatExample()
    return asyncio.run(chat.start_discussion(task))
