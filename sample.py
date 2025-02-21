from autogen_core import RoutedAgent, rpc, MessageContext
from dataclasses import dataclass
from autogen_agentchat.teams import RoundRobinGroupChat
from sugc import GroupChatAsAnAgent
import asyncio

# メッセージ型の定義
@dataclass
class QueryMessage:
    content: str

@dataclass
class ResponseMessage:
    content: str

# GroupChatAsAnAgentを実行するエージェント
class GroupChatExecutorAgent(RoutedAgent):
    def __init__(self):
        self.name = "executor"
        self.description = "GroupChat Executor Agent"  # descriptionを追加
        super().__init__(self.description)

    @rpc
    async def process_query(self, message: QueryMessage, ctx: MessageContext) -> ResponseMessage:
        result = GroupChatAsAnAgent(query=message.content, config="Gr2")
        return ResponseMessage(content=result)

class ResponseAgent(RoutedAgent):
    def __init__(self):
        self.name = "responder"
        self.description = "Response Agent"  # descriptionを追加
        super().__init__(self.description)

    @rpc
    async def respond(self, message: ResponseMessage, ctx: MessageContext) -> QueryMessage:
        return QueryMessage(content=f"前回の結果について詳しく説明してください: {message.content}")
from autogen_core import SingleThreadedAgentRuntime

async def setup_chat():
    runtime = SingleThreadedAgentRuntime()
    runtime.start()

    # エージェントの登録
    await GroupChatExecutorAgent.register(
        runtime=runtime,
        type="executor",
        factory=lambda: GroupChatExecutorAgent()
    )

    await ResponseAgent.register(
        runtime=runtime,
        type="responder",
        factory=lambda: ResponseAgent()
    )

    # 実際のAgentインスタンスを取得
    executor = await runtime.try_get_underlying_agent_instance(await runtime.get("executor"))
    responder = await runtime.try_get_underlying_agent_instance(await runtime.get("responder"))

    # RoundRobinGroupChatの作成
    chat = RoundRobinGroupChat(
        participants=[executor, responder],
        max_turns=3
    )

    return chat, runtime
# 使用例
async def run_chat():
    chat, runtime = await setup_chat()
    initial_query = QueryMessage(content="営業Level3の目標が知りたいです。")
    result = await chat.run(initial_query)
    await runtime.stop()
    return result

if __name__ == "__main__":
    asyncio.run(run_chat())
