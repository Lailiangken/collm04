import asyncio
import os
import logging
from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_functions.load_agents import load_agents_from_directory
from autogen_functions.load_model import load_model_from_config
from autogen_functions.logging_agents import LoggingAssistantAgent, LoggingUserProxyAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent

class GroupChatExample:
    def __init__(self, chat_mode: str = "通常チャット"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, "agents")
        
        self.model_client = load_model_from_config("gpt-4o_1")
        self.agents = load_agents_from_directory(agents_dir, self.model_client, agent_class=LoggingAssistantAgent)
        self.runtime = SingleThreadedAgentRuntime()
        

        if chat_mode == "コード実行チャット":
            host_work_dir = os.getenv('WORK_DIR', '/default/path')
            container_work_dir = 'workspace'
            
            self.code_executor = DockerCommandLineCodeExecutor(
                image="python:3-slim",
                timeout=60,
                work_dir=container_work_dir,
                bind_dir=host_work_dir,
                auto_remove=False
            )
            
            self.code_executor_agent = CodeExecutorAgent(
                "executor",
                code_executor=self.code_executor,
                description="Executes Python code and returns the output."
            )
            participants = self.agents + [self.code_executor_agent]
        else:
            participants = self.agents

        self.termination = TextMentionTermination("TERMINATE")
        
        self.team = SelectorGroupChat(
            participants=participants,
            model_client=self.model_client,
            termination_condition=self.termination,
            selector_prompt="""You are in a role play game. The following roles are available:
{roles}.
Read the following conversation. Then select the next role from {participants} to play. Only return the role.

{history}

Read the above conversation. Then select the next role from {participants} to play. Only return the role.
""",
            allow_repeated_speaker=False
        )

    async def start_discussion(self, task: str) -> str:
        logging.info("チャットを開始します...")
        if hasattr(self, 'code_executor'):
            async with self.code_executor:
                result = await self.team.run(task=task)
        else:
            result = await self.team.run(task=task)
        logging.info("チャットが終了しました。")
        return result

def run_group_chat(task: str, chat_mode: str = "通常チャット") -> str:
    chat = GroupChatExample(chat_mode=chat_mode)
    return asyncio.run(chat.start_discussion(task))

if __name__ == "__main__":
    task = "Pythonを使って'Hello, World!'を出力するプログラムを作成し、実行してください。"
    result = run_group_chat(task)
    print(result)
