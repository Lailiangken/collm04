import streamlit as st
import os
import shutil
from pathlib import Path
from datetime import datetime
from autogen_functions.factory import create_llm_function
from dotenv import load_dotenv
import inspect
from typing import get_type_hints

# 環境変数の読み込み
load_dotenv()


def save_generated_result(result: str, query: str, chat_history: list, function_type: str, file_extension: str = "py") -> str:
    """
    生成結果を保存する汎用的な関数
    
    Args:
        result: 生成された結果（コードやテキストなど）
        query: ユーザーからの入力クエリ
        chat_history: エージェント間の会話履歴
        function_type: 機能の種類（'code_generator', 'code_review'など）
        file_extension: 保存するファイルの拡張子（デフォルト: py）
    
    Returns:
        str: 保存されたファイルのパス
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized_query = "".join(c for c in query[:30] if c.isalnum() or c in (' ', '_')).strip()
    
    # 機能タイプごとのフォルダを作成
    output_dir = Path(f"output/{function_type}/{timestamp}_{sanitized_query}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 結果の保存
    output_file = output_dir / f"generated_result.{file_extension}"
    with open(output_file, "w") as f:
        f.write(result)
    
    # クエリの保存
    query_file = output_dir / "query.txt"
    with open(query_file, "w") as f:
        f.write(query)
    
    # 会話履歴の保存
    chat_file = output_dir / "conversation.txt"
    with open(chat_file, "w") as f:
        for message in chat_history:
            f.write(f"Role: {message.get('role', 'unknown')}\n")
            f.write(f"Content:\n{message.get('content', '')}\n")
            f.write("-" * 80 + "\n")
    
    return str(output_file)

def get_function_parameters(function_class):
    """クラスの__call__メソッドのパラメータ情報を取得"""
    signature = inspect.signature(function_class.__call__)
    type_hints = get_type_hints(function_class.__call__)
    
    parameters = {}
    for name, param in signature.parameters.items():
        if name != 'self':
            parameters[name] = {
                'type': type_hints.get(name, str),
                'default': param.default if param.default != param.empty else None,
                'required': param.default == param.empty
            }
    return parameters

def create_input_field(name: str, param_info: dict):
    """パラメータの型に応じた入力フィールドを生成"""
    param_type = param_info['type']
    
    if param_type == str:
        if 'code' in name.lower():
            return st.text_area(f"{name}", height=300)
        elif 'requirement' in name.lower():
            return st.text_area(f"{name}", height=300)
        else:
            return st.text_input(f"{name}")
    elif param_type == int:
        return st.number_input(f"{name}", step=1)
    elif param_type == float:
        return st.number_input(f"{name}", step=0.1)
    elif param_type == bool:
        return st.checkbox(f"{name}")
    elif param_type == list:
        return st.text_area(f"{name} (カンマ区切りで入力)", height=100)
    else:
        return st.text_input(f"{name}")

def cleanup_working_directory(working_dir: str = "coding") -> None:
    """
    ワーキングフォルダの中身を削除する
    
    Args:
        working_dir: 削除対象のディレクトリ名
    """
    working_path = Path(working_dir)
    if working_path.exists():
        shutil.rmtree(working_path)
        working_path.mkdir(exist_ok=True)

from autogen_functions.factory import get_available_functions

def main():
    st.title("Code Assistant")
    
    api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    functions = get_available_functions()
    selected_function = st.selectbox(
        "機能を選択してください",
        options=list(functions.keys())
    )
    
    # 選択された機能のクラスを取得
    function_class = create_llm_function(selected_function)
    
    if function_class:
        parameters = get_function_parameters(function_class)
        input_values = {}
        
        for name, param_info in parameters.items():
            input_values[name] = create_input_field(name, param_info)

        if 'processing' not in st.session_state:
            st.session_state.processing = False

        button_text = "処理中..." if st.session_state.processing else "実行"
        if st.button(button_text, disabled=st.session_state.processing) and api_key and all(v for v in input_values.values() if v is not None):
            try:
                st.session_state.processing = True
                with st.spinner("処理中..."):
                    instance = function_class()
                    result = instance(**input_values)
                    print(result)
                    
                    if selected_function == 'コード生成':
                        saved_path = save_generated_result(
                            result=result,
                            query=input_values.get('requirements', ''),
                            chat_history=instance.get_chat_history(),
                            function_type='code_generator',
                            file_extension="py"
                        )
                        st.markdown("### 生成されたコード")
                        st.code(result, language="python")
                        st.markdown(f"### 保存場所\n`{saved_path}`")
                    elif selected_function == 'コードレビュー':
                        saved_path = save_generated_result(
                            result=result,
                            query=input_values.get('code', ''),
                            chat_history=instance.get_chat_history(),
                            function_type='code_review',
                            file_extension="md"
                        )
                        st.markdown(result)
                    elif selected_function in ['グループコード生成', 'グループチャット']:
                        saved_path = save_generated_result(
                            result=result,
                            query=input_values.get('requirements', ''),
                            chat_history=instance.get_chat_history(),
                            function_type='group_chat',
                            file_extension="md"
                        )
                        st.markdown(result)                
                st.session_state.processing = False
                cleanup_working_directory()
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.session_state.processing = False
                cleanup_working_directory()
    if not api_key:
        st.warning("OpenAI APIキーを入力してください。")
if __name__ == "__main__":
    main()  