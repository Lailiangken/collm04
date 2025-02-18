import os
import re
import logging
from pathlib import Path
from typing import List
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.code_executor import CodeBlock

def extract_markdown_code_blocks(markdown_text: str) -> List[CodeBlock]:
    pattern = re.compile(r"(?:\s*([\w\+\-]+))?\n([\s\S]*?)")
    matches = pattern.findall(markdown_text)
    code_blocks: List[CodeBlock] = []
    for match in matches:
        language = match[0].strip().lower() if match[0] else ""
        code_content = match[1]
        code_blocks.append(CodeBlock(code=code_content, language=language))
    return code_blocks

async def main():
    # 環境変数から作業ディレクトリを取得
    host_work_dir = os.getenv('WORK_DIR', '/default/path')  # デフォルトパスを指定可能
    container_work_dir = 'workspace'  # コンテナ内での作業ディレクトリ

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Binding host directory {host_work_dir} to container {container_work_dir}")

    code_executor = DockerCommandLineCodeExecutor(
        image="python:3-slim",
        timeout=60,
        work_dir=container_work_dir,
        bind_dir=host_work_dir
    )
    
    async with code_executor:
        # CodeExecutorAgentの設定
        code_executor_agent = CodeExecutorAgent("executor", code_executor=code_executor)
        
        # モデルクライアントの設定
        model_client = OpenAIChatCompletionClient(model="gpt-4")
        assistant = AssistantAgent("assistant", model_client=model_client)

        # メッセージの作成
        message = TextMessage(
            content="Pythonを使って完全数を3個出力するコードを作成してください",
            source="user"
        )
        
        # AssistantAgentを使用してコードを生成
        async for response in assistant.run_stream(task=message, cancellation_token=CancellationToken()):
            if hasattr(response, 'messages'):
                for msg in response.messages:
                    if hasattr(msg, 'content'):
                        content = msg.content
                        print("生成されたコード:")
                        print(content)
                        code_blocks = extract_markdown_code_blocks(content)
                        if code_blocks:
                            # CodeExecutorAgentを使用してコードを実行
                            executor_result = await code_executor_agent.on_messages(
                                [TextMessage(content=content, source="assistant")],
                                cancellation_token=CancellationToken()
                            )
                            print("実行結果:")
                            print(executor_result.chat_message.content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())