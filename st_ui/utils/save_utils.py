import os
import json
import streamlit as st
from datetime import datetime

def save_result(formatted_result, chat_info, last_result):
    if formatted_result:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join('output', timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        result_path = os.path.join(output_dir, 'chat_history.md')
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        
        chatinfo_path = os.path.join(output_dir, 'chat_info.json')
        with open(chatinfo_path, 'w', encoding='utf-8') as f:
            json.dump(chat_info, f, ensure_ascii=False, indent=2)
        
        last_result_path = os.path.join(output_dir, 'last_result.md')
        with open(last_result_path, 'w', encoding='utf-8') as f:
            f.write(last_result)

        st.success(f"結果を保存しました: {result_path}")
