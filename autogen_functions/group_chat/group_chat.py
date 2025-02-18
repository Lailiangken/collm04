import asyncio
import os
import logging
from autogen_core import SingleThreadedAgentRuntime, EVENT_LOGGER_NAME
from autogen_agentchat.teams import SelectorGroupChat, MagenticOneGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_functions.load_agents import load_agents_from_directory
from autogen_functions.load_model import load_model_from_config
from autogen_functions.logging_agents import LoggingAssistantAgent, LoggingUserProxyAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.base import TaskResult

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(EVENT_LOGGER_NAME)

class GroupChatExample:
    def __init__(self, group_name: str = "Agents", use_web_surfer: bool = False, use_code_executor: bool = False, chat_type: str = "selector"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agents_dir = os.path.join(current_dir, group_name, "agents")
        
        self.model_client = load_model_from_config("gpt-4o_1")
        self.agents = load_agents_from_directory(agents_dir, self.model_client, agent_class=LoggingAssistantAgent)
        self.runtime = SingleThreadedAgentRuntime()
        participants = self.agents.copy()

        if use_code_executor:
            host_work_dir = os.getenv('WORK_DIR', '/default/path')
            container_work_dir = 'workspace'
            
            self.code_executor = DockerCommandLineCodeExecutor(
                image="python:3-slim",
                timeout=60,
                work_dir=container_work_dir,
                bind_dir=host_work_dir
            )
            
            self.code_executor_agent = CodeExecutorAgent(
                "executor",
                code_executor=self.code_executor,
                description="Executes Python code and returns the output."
            )
            participants.append(self.code_executor_agent)
            
        if use_web_surfer:
            self.web_surfer = MultimodalWebSurfer(
                "web_surfer",
                description="A web surfer that can search the web and return the results.",
                model_client=self.model_client
            )
            participants.append(self.web_surfer)
            

        self.termination = TextMentionTermination("TERMINATE")
        
        if chat_type == "selector":
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
        else:  # magentic
            self.team = MagenticOneGroupChat(
                participants=participants,
                model_client=self.model_client,
            )

    async def start_discussion(self, task: str) -> str:
        logger.info("チャットを開始します...")
        if hasattr(self, 'code_executor'):
            async with self.code_executor:
                result = await self.team.run(task=task)
        else:
            result = await self.team.run(task=task)
        logger.info("チャットが終了しました。")
        return result

def run_group_chat(
    task: str, 
    group_name: str = "Agents", 
    use_web_surfer: bool = False, 
    use_code_executor: bool = False, 
    chat_type: str = "selector"
) -> str:
    chat = GroupChatExample(
        group_name=group_name,
        use_web_surfer=use_web_surfer,
        use_code_executor=use_code_executor,
        chat_type=chat_type
    )
    return asyncio.run(chat.start_discussion(task))
if __name__ == "__main__":
    task = "Pythonを使って'Hello, World!'を出力するプログラムを作成し、実行してください。"
    # セレクターチャットの実行
    result_selector = run_group_chat(task, chat_type="selector")
    print("Selector Chat Result:", result_selector)
    
    # magenticチャットの実行
    result_magentic = run_group_chat(task, chat_type="magentic")
    print("magentic Chat Result:", result_magentic)

class GroupChatRunner:
    def __init__(self):
        self.message_callback = None
        self.result_callback = None
    
    def set_callbacks(self, message_callback, result_callback):
        self.message_callback = message_callback
        self.result_callback = result_callback
    
    async def run_chat(self, task: str, chat_type: str, use_web_surfer: bool, use_code_executor: bool, group_name: str):
        chat = GroupChatExample(
            chat_type=chat_type,
            use_web_surfer=use_web_surfer,
            use_code_executor=use_code_executor,
            group_name=group_name
        )

        
        if hasattr(chat, 'code_executor'):
            async with chat.code_executor:
                stream = chat.team.run_stream(task=task)
                return await self._process_stream(stream)
        else:
            stream = chat.team.run_stream(task=task)
            return await self._process_stream(stream)


    async def _process_stream(self, stream):
        final_message = None
        messages = []
        try:
            async for message in stream:
                if isinstance(message, TaskResult):
                    if message.messages:
                        final_message = message.messages[-1]
                        if self.result_callback:
                            self.result_callback(final_message.content)
                
                if self.message_callback:
                    await self.message_callback(message)  # awaitを追加
                messages.append(message)
            
            return messages, final_message.content if final_message else None
        except Exception as e:
            # Handle the exception appropriately
            print(f"An error occurred: {e}")
            return messages, None
