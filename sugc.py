import asyncio
import os
import json
from autogen_functions.group_chat.group_chat import GroupChatRunner

def load_settings(settings_path: str) -> dict:
    with open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)

async def GroupChatWrapper(query:str,message_stream: bool = False, config: str = "Gr2") -> str:
    # GroupChatRunnerのインスタンス化
    runner = GroupChatRunner()
    
    # コールバック関数の定義
    if message_stream:
        async def print_message(message_stream):
            print("\n=== チャット進行状況 ===")
            print(message_stream)
            
        def print_result(result):
            print("\n=== 最終結果 ===")
            print(result)

        # コールバックの設定
        runner.message_callback = print_message
        runner.result_callback = print_result
    
    # 設定ファイルからパラメータを読み込み
    settings_path_folder = "groupchats"
    settings_path = os.path.join(settings_path_folder, config + ".json")
    settings = load_settings(settings_path)
    full_query = settings['query_prefix'] + query
    # チャット実行と結果取得
    results = await runner.stream_chat(
        task=full_query,
        chat_type=settings['chat_type'],
        use_web_surfer=settings['use_web_surfer'],
        use_code_executor=settings['use_code_executor'],
        group_name=settings['group_name'],
        model_name=settings['model_name']
    )
    # print(f"chat_history:{results["chat_history"]}")
    # print(f"last_result:{results["last_result"]}")
    return results

def GroupChatAsAnAgent(query:str, config: str = "Gr2") -> str:
    results = asyncio.run(GroupChatWrapper(query=query,config=config))
    return results["last_result"]
    
if __name__ == "__main__":
    query = "営業Level3の目標が知りたいです。"
    result = GroupChatAsAnAgent(query)
    print(result)