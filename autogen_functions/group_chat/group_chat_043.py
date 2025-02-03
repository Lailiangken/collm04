import asyncio
import os
import logging
import tempfile
from pathlib import Path
from autogen_core import SingleThreadedAgentRuntime, CancellationToken
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_functions.load_model import load_model_from_config
from autogen_functions.load_agents import load_agents_from_directory
from autogen_functions.logging_agents import LoggingAssistantAgent, LoggingUserProxyAgent

class GroupChatExample:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, "agents")
        self.work_dir = Path(tempfile.mkdtemp())
        self.work_dir.mkdir(exist_ok=True)
        
        self.runtime = SingleThreadedAgentRuntime()
        self.model_client = load_model_from_config("gpt-4o_1")
        
        # エージェントをJSONファイルから読み込む
        self.agents = load_agents_from_directory(
            agents_dir, 
            self.model_client, 
            agent_class=LoggingAssistantAgent
        )
        
        self.user_proxy = LoggingUserProxyAgent(
            name="user_proxy",
            description="A user proxy that helps with the task."
        )
        
        self.code_executor = DockerCommandLineCodeExecutor(
            work_dir=str(self.work_dir),
            image="python:3-slim",
            timeout=300
        )
        
        self.code_executor_agent = CodeExecutorAgent(
            name="code_executor",
            code_executor=self.code_executor
        )
        
        self.termination = TextMentionTermination("TERMINATE")
        self.team = RoundRobinGroupChat(
            participants=self.agents + [self.user_proxy, self.code_executor_agent],
            termination_condition=self.termination
        )

    async def start_discussion(self, task: str) -> str:
        logging.info("チャットを開始します...")
        self.runtime.start()
        
        try:
            async with self.code_executor:
                result = await self.team.run(task=task)
                await self.runtime.stop_when_idle()
                return result
        except Exception as e:
            logging.error(f"エラーが発生しました: {str(e)}")
            raise
        finally:
            await self.code_executor.stop()

def run_group_chat(task: str) -> str:
    chat = GroupChatExample()
    return asyncio.run(chat.start_discussion(task))

if __name__ == "__main__":
    task = "Pythonを使って'Hello, World!'を出力するプログラムを作成し、実行してください。"
    result = run_group_chat(task)
    print(result)
