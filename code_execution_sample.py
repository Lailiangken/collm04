import re
import tempfile
from pathlib import Path
from typing import List
from autogen_core import SingleThreadedAgentRuntime, CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.code_executor import CodeBlock



def extract_markdown_code_blocks(markdown_text: str) -> List[CodeBlock]:
    pattern = re.compile(r"```(?:\s*([\w\+\-]+))?\n([\s\S]*?)```")
    matches = pattern.findall(markdown_text)
    code_blocks: List[CodeBlock] = []
    for match in matches:
        # 言語指定を適切に変換
        language = match[0].strip().lower() if match[0] else ""
        if language == "python":
            language = "py"  # pythonをpyに変換
        code_content = match[1]
        code_blocks.append(CodeBlock(code=code_content, language=language))
    return code_blocks

async def main():
    # 作業ディレクトリを絶対パスで指定
    
    code_executor = DockerCommandLineCodeExecutor(

        image="python:3-slim",
        timeout=60,
        )
    
    async with code_executor:
        code_executor_agent = CodeExecutorAgent("executor", code_executor=code_executor)
        model_client = OpenAIChatCompletionClient(model="gpt-4")
        assistant = AssistantAgent("assistant", model_client=model_client)

        message = TextMessage(
            content="Pythonを使って'フィボナッチ数列を15桁'出力するプログラムを作成してください。",
            source="user",
            work_dir="workspace"
        )
        
        async for response in assistant.run_stream(task=message, cancellation_token=CancellationToken()):
            print(response)
            if hasattr(response, 'messages'):
                for msg in response.messages:
                    if hasattr(msg, 'content'):
                        content = msg.content
                        code_blocks = extract_markdown_code_blocks(content)
                        if code_blocks:
                            executor_result = await code_executor.execute_code_blocks(
                                code_blocks, 
                                cancellation_token=CancellationToken()
                                
                            )
                            print("実行結果:")
                            print(executor_result.output)


    # async withを使用しているため、明示的なstopは不要


    # async withを使用しているため、明示的なstopは不要

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
