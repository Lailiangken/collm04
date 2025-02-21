import asyncio
import os
from autogen_functions.group_chat.group_chat import GroupChatRunner

async def main():
    # GroupChatRunnerのインスタンス化
    runner = GroupChatRunner()
    
    # コールバック関数の定義
    async def print_message(message_stream):
        print("\n=== チャット進行状況 ===")
        print(message_stream)
        
    def print_result(result):
        print("\n=== 最終結果 ===")
        print(result)
    
    # コールバックの設定
    runner.message_callback = print_message
    runner.result_callback = print_result
    
    # パラメータ設定
    task = "Pythonを使って'Hello, World!'を出力するプログラムを作成し、実行してください。"
    chat_type = "selector"
    use_web_surfer = False
    use_code_executor = True
    group_name = "default"
    model_name = "gpt-4o_1"

    # チャット実行と結果取得
    result = await runner.stream_chat(
        task=task,
        chat_type=chat_type,
        use_web_surfer=use_web_surfer,
        use_code_executor=use_code_executor,
        group_name=group_name,
        model_name=model_name
    )
    print(f"chat_history:{result["chat_history"]}")
    print(f"last_result:{result["last_result"]}")


if __name__ == "__main__":
    asyncio.run(main())
    