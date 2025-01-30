from typing import List
import asyncio
from autogen_core.code_executor import CodeBlock, CodeExecutor, CodeResult
from autogen_core import CancellationToken

class AutogenCodeExecutor(CodeExecutor):
    """Autogenのコード実行エンジン"""
    
    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout

    async def execute_code_blocks(
        self, 
        code_blocks: List[CodeBlock],
        cancellation_token: CancellationToken
    ) -> CodeResult:
        """
        コードブロックを実行して結果を返す
        
        Args:
            code_blocks: 実行するコードブロックのリスト
            cancellation_token: キャンセルトークン
            
        Returns:
            CodeResult: 実行結果
        """
        output = []
        exit_code = 0

        for block in code_blocks:
            if block.language.lower() != "python":
                continue
                
            try:
                # 非同期実行のためにイベントループを取得
                loop = asyncio.get_event_loop()
                
                # コードをローカルスコープで実行
                local_vars = {}
                exec_result = await asyncio.wait_for(
                    loop.run_in_executor(None, exec, block.code, {}, local_vars),
                    timeout=self.timeout
                )
                
                # 実行結果を取得
                if 'result' in local_vars:
                    output.append(str(local_vars['result']))
                else:
                    output.append("Code executed successfully")
                    
            except asyncio.TimeoutError:
                exit_code = 1
                output.append(f"Execution timed out after {self.timeout} seconds")
                break
            except Exception as e:
                exit_code = 1
                output.append(f"Error: {str(e)}")
                break

        return CodeResult(
            exit_code=exit_code,
            output="\n".join(output)
        )

    async def restart(self) -> None:
        """実行環境をリセット"""
        pass
