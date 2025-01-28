from ..base.llm_base import LLMBaseFunction
import autogen.agentchat
import os

class GroupChatGenerator(LLMBaseFunction):
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__(model_name)
        
        # GPT-4の設定を正しく構築
        self.gpt4_config = {
            "cache_seed": 42,
            "temperature": 0,
            "config_list": [{
                "model": model_name,
                "api_key": os.environ["OPENAI_API_KEY"]
            }],
            "timeout": 120,
        }
        
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
        
        # 正しい設定でマネージャーを初期化
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.gpt4_config
        )
