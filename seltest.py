import os
import logging
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken

async def main():
    # 環境変数から作業ディレクトリを取得
    host_work_dir = os.getenv('WORK_DIR', '/default/path')  # デフォルトパスを指定可能
    container_work_dir = 'workspace'  # コンテナ内での作業ディレクトリ

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Binding host directory {host_work_dir} to container {container_work_dir}")

    # モデルクライアントの設定
    model_client = OpenAIChatCompletionClient(model="gpt-4")

    # DockerCommandLineCodeExecutorの設定
    code_executor = DockerCommandLineCodeExecutor(
        image="python:3-slim",
        timeout=60,
        work_dir=container_work_dir,
        bind_dir=host_work_dir,
        auto_remove=False
    )

    async with code_executor:  # コンテナの初期化とクリーンアップを確実に行う
        # エージェントの設定
        agent1 = AssistantAgent(
            "Agent1",
            model_client,
            description="エンジニアです。問題に対してコードを書くことで問題解決を行います。",
            system_message="エンジニア。タスクを解決するためにpython/shellコードを書く。スクリプトの種類を指定するコードブロックでコードを囲みます。実行環境はリモート環境であり、操作対象のファイルなどは存在しません。テストデータ等を作成する必要がある場合は、その作成のためのコードも作成してください。ユーザーはあなたのコードを修正できません。ですから、他の人が修正しなければならないような不完全なコードを提案しないでください。実行者によって実行されることを意図していないコードブロックは使わないでください。\n一つのレスポンスに複数のコードブロックを含めないでください。他の人に結果をコピー＆ペーストするよう求めないこと。エクゼキューターが返す実行結果をチェックしてください。\n結果がエラーを示している場合は、エラーを修正してコードを出力し直してください。部分的なコードやコードの変更ではなく、完全なコードを提案してください。エラーが修正できない場合、またはコードが正常に実行された後でもタスクが解決されない場合は、問題を分析し、仮定を再検討し、必要な追加情報を収集し、別のアプローチを考える。プログラムが正しく実行され、テストが完了したら、TERMINATEと記載してください。"
        )
        agent2 = CodeExecutorAgent(
            "Agent2",
            code_executor=code_executor,
            description="Executes Python code.",
        )
        # グループチャットの設定
        termination_condition = TextMentionTermination("TERMINATE")  # 適切な終了条件を設定
        team = SelectorGroupChat(
            participants=[agent1, agent2],
            model_client=model_client,
            termination_condition=termination_condition,
            selector_prompt="""You are in a role play game. The following roles are available:
{roles}.
Read the following conversation. Then select the next role from {participants} to play. Only return the role.

{history}

Read the above conversation. Then select the next role from {participants} to play. Only return the role.
""",
            allow_repeated_speaker=False
        )

        # メッセージの作成
        message = TextMessage(
            content="フォルダに含まれるファイルを拡張子ごとに分類しフォルダ分けするプログラムを作成してください。",
            source="user"
        )
        
        # グループチャットを実行
        async for response in team.run_stream(task=message, cancellation_token=CancellationToken()):
            print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())