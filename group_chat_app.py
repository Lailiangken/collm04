import streamlit as st
from st_ui.render.render_sidebar import render_sidebar
from st_ui.render.render_main import render_main_content
import os
from datetime import datetime
import json

def save_result(formatted_result,chat_info,last_result):
    if formatted_result:
        # 現在の日時を取得してフォルダ名を生成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # output/[日時名フォルダ]のパスを作成
        output_dir = os.path.join('output', timestamp)
        
        # フォルダが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 結果をファイルに保存
        result_path = os.path.join(output_dir, 'chat_history.md')
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        
        chatinfo_path = os.path.join(output_dir, 'chat_info.json')
        with open(chatinfo_path, 'w', encoding='utf-8') as f:
            json.dump(chat_info, f, ensure_ascii=False, indent=2)
        
        last_result_path = os.path.join(output_dir, 'last_result.md')
        with open(last_result_path, 'w', encoding='utf-8') as f:
            f.write(last_result)

        # 保存完了メッセージを表示
        st.success(f"結果を保存しました: {result_path}")

def main():
    selected_group = render_sidebar()
    if not selected_group:
        return
    
    formatted_result ,chat_info ,last_result = render_main_content(selected_group)
    save_result(formatted_result,chat_info,last_result)

if __name__ == "__main__":
    main()
