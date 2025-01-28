from ..base.llm_base import LLMBaseFunction
import autogen_agentchat as autogen

class GroupChatGenerator(LLMBaseFunction):
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name)
        
        # グループチャットの設定
        self.group_chat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                *self.assistants.values()
            ],
            messages=[],
            max_round=12,
            speaker_selection_method="round_robin",
            allow_repeat_speaker=False
        )
        
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.config_list
        )

    def __call__(self, requirements: str) -> str:
        """グループチャットによる開発プロセスを実行"""
        self.conversation_result = self.user_proxy.initiate_chat(
            self.manager,
            message=f"""
開発要件について議論を行い、実装してください。

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
