from ..base.llm_base import LLMBaseFunction
#このファイルは基底クラスLLMBaseFunctionを継承し、コード生成に特化した機能を提供します。主要な処理は__call__メソッドで行われ、AIとの対話からコードブロックを抽出する機能を実装しています。
class CodeGeneratorFunction(LLMBaseFunction):
    def __call__(self, requirements: str) -> str:
        try:
            self.conversation_result = self.user_proxy.initiate_chat(
                self.assistants['code_generator'],
                message=f"""
以下の要件に基づいてPythonコードを生成してください。
コードブロックのみを出力してください。説明は不要です。

要件:
{requirements}
                """,
                clear_history=True
            )
            
            # 会話履歴から全てのコードブロックを抽出
            code_blocks = []
            for message in self.conversation_result.chat_history:
                content = message['content']
                lines = content.split('\n')
                in_code_block = False
                current_block = []
                
                for line in lines:
                    if line.strip().startswith('```'):
                        if in_code_block:
                            # コードブロックの終了を検出したら、現在のブロックを保存
                            code_blocks.append('\n'.join(current_block))
                            current_block = []
                        in_code_block = not in_code_block
                    elif in_code_block:
                        # コードブロック内の行を収集
                        current_block.append(line)
            
            # 最後のコードブロックを返す（最終的な生成結果）
            if code_blocks:
                return code_blocks[-1]
            
            # コードブロックが見つからない場合は、最後のメッセージを返す
            return self.conversation_result.chat_history[-1]['content']

        except Exception as e:
            return f"コード生成中にエラーが発生しました: {str(e)}"         