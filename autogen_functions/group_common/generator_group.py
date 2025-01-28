from ..base.llm_base import LLMBaseFunction
import autogen_agentchat as autogen
import os

class CommonGroupChatGenerator(LLMBaseFunction):
    def __init__(self, model_name: str = "o1-mini-2024-09-12"):
        super().__init__(model_name)
        # グループチャットの設定
        # GPT-4の設定を正しく構築
        self.gpt4_config = {
            "cache_seed": 42,
            "config_list": [{
                "model": model_name,
                "api_key": os.environ["OPENAI_API_KEY"]
            }],
            "timeout": 120,
        }
        
        # グループチャッ
        # グループチャットの設定
        self.group_chat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                *self.assistants.values()
            ],
            messages=[],
            max_round=100
        )
        
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.gpt4_config
        )

    def __call__(self, requirements: str) -> str:
        """グループチャットによる開発プロセスを実行"""
        self.conversation_result = self.user_proxy.initiate_chat(
            self.manager,
            message=f"""

要件:
{requirements}

各メンバーは自身の専門性を活かして貢献してください。
            """,
            clear_history=True
        )
        
        return self._format_chat_history()
        
    def _format_chat_history(self) -> str:
        """会話履歴を整形"""
        result = "# 開発プロジェクト記録\n\n"
        
        for msg in self.group_chat.messages:
            if msg.get("role") != "system":
                result += f"## {msg.get('name', 'System')}\n"
                result += f"{msg['content']}\n\n"
                
        return result
