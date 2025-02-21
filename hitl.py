import asyncio
from tools.sugc import GroupChatWrapper

class HitlChat:
    def __init__(self, config: str = "Gr2"):
        self.config = config
        self.chat_history = []

    def format_chat_history(self, chat_history):
        formatted_history = ""
        for message in chat_history:
            if hasattr(message, 'content') and hasattr(message, 'source'):
                formatted_history += f"\n{message.source}: {message.content}"
        return formatted_history

    async def start_interactive_chat(self, initial_task: str):
        while True:
            if not self.chat_history:
                results = await GroupChatWrapper(
                    query=initial_task,
                    message_stream=True,
                    config=self.config
                )
            else:
                history_text = self.format_chat_history(self.chat_history)
                query_with_history = f"{initial_task}"
                
                results = await GroupChatWrapper(
                    query=query_with_history,
                    message_stream=True,
                    config=self.config,
                )
            
            self.chat_history = results["chat_history"]
            print(self.chat_history)
            
            user_input = input("\nEnter your feedback (type 'exit' to leave): ")
            if user_input.lower().strip() == "exit":
                break
            initial_task = user_input

async def main():
    chat = HitlChat(config="call_center")
    initial_task = "このグループチャットを1人のオペレーターとして扱い、ユーザの職位、メールアドレス、電話番号を聞き出すための質問を出力してください。"
    await chat.start_interactive_chat(initial_task)

if __name__ == "__main__":
    asyncio.run(main())