from dataclasses import dataclass
import re
from typing import List
from autogen_core import RoutedAgent, MessageContext, event
from autogen_core.code_executor import CodeBlock, CodeExecutor

@dataclass
class ExecutorMessage:
    content: str

class ExecutorAgent(RoutedAgent):
    """コード実行を行うエージェント"""
    
    def __init__(self, description: str, code_executor: CodeExecutor) -> None:
        super().__init__(description)
        self._code_executor = code_executor

    @event
    async def handle_code(self, message: ExecutorMessage, ctx: MessageContext) -> None:
        code_blocks = self.extract_markdown_code_blocks(message.content)
        
        if code_blocks:
            result = await self._code_executor.execute_code_blocks(
                code_blocks, 
                cancellation_token=ctx.cancellation_token
            )
            
            await self.send_message(
                ExecutorMessage(content=result.output),
                ctx.sender
            )

    @staticmethod
    def extract_markdown_code_blocks(markdown_text: str) -> List[CodeBlock]:
        pattern = re.compile(r"(?:\s*([\w\+\-]+))?\n([\s\S]*?)")
        matches = pattern.findall(markdown_text)
        return [CodeBlock(code=match[1], language=match[0].strip() if match[0] else "") for match in matches]