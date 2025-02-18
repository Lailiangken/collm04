import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

async def main():
    # Azure OpenAIクライアントの設定
    model_client = AzureOpenAIChatCompletionClient(
        azure_endpoint="https://llm-deloitte-gpt4-verification.openai.azure.com/",
        azure_deployment="gpt-4o",
        model="gpt-4",
        api_version="2024-06-01",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "GPT_4"
        }
    )
    # エージェントの作成
    developer = AssistantAgent(
        name="developer",
        description="エンジニア。タスクを解決するためにpython/shellコードを書く。",
        system_message="エンジニア。タスクを解決するためにpython/shellコードを書く。スクリプトの種類を指定するコードブロックでコードを囲みます。",
        model_client=model_client,
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    reviewer = AssistantAgent(
        name="reviewer",
        description="コードレビュアー。コードの品質をチェックし改善点を提案する。",
        system_message="コードレビュアー。提案されたコードの品質をチェックし、改善点を指摘します。",
        model_client=model_client,
        model_client_stream=True
    )

    # 終了条件の設定
    termination = TextMentionTermination("TERMINATE")

    # RoundRobinGroupChatの設定
    team = RoundRobinGroupChat(
        participants=[developer, reviewer],
        termination_condition=termination
    )

    # チャットの実行
    result = await team.run(
        task="Pythonを使って'Hello, World!'を出力するプログラムを作成し、コードレビューを行ってください。",
        cancellation_token=CancellationToken()
    )

    print("Chat completed with result:", result)

if __name__ == "__main__":
    asyncio.run(main())
