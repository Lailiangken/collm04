from ..base.llm_base import LLMBaseFunction

class CodeReviewFunction(LLMBaseFunction):
    def __call__(self, code: str) -> str:
        try:
            review_result = self.user_proxy.initiate_chat(
                self.assistants['code_reviewer'],
                message=f"このコードをレビューしてください:\n{code}",
                clear_history=True
            )
            
            review_content = review_result.chat_history[-1]['content']
            
            improvement_result = self.user_proxy.initiate_chat(
                self.assistants['code_improver'],
                message=f"以下のレビュー結果に基づいて、具体的な改善案を提示してください:\n\n{review_content}",
                clear_history=True
            )
            
            improvement_content = improvement_result.chat_history[-1]['content']
            
            return f"""
レビュー結果:
{review_content}

改善提案:
{improvement_content}
"""
        except Exception as e:
            return f"レビュー中にエラーが発生しました: {str(e)}"
