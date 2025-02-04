import streamlit as st
from autogen_functions.group_chat.group_chat_043 import run_group_chat

def format_task_result(task_result):
    """Format the TaskResult object into Markdown."""
    md_output = "# 議論の結果\n\n"
    
    for message in task_result.messages:
        md_output += f"## {message.source.capitalize()}\n"
        md_output += f"{message.content}\n\n"
    
    return md_output

def main():
    st.title("Group Chat Assistant")

    # チャットモードの選択
    chat_mode = st.selectbox(
        "チャットモードを選択してください:",
        ["通常チャット", "コード実行チャット"]
    )

    task = st.text_area("議論するタスクや話題を入力してください:", height=200)

    if 'processing' not in st.session_state:
        st.session_state.processing = False

    button_text = "処理中..." if st.session_state.processing else "実行"
    if st.button(button_text, disabled=st.session_state.processing) and task:
        try:
            st.session_state.processing = True
            with st.spinner("処理中..."):
                task_result = run_group_chat(task, chat_mode=chat_mode)
                formatted_result = format_task_result(task_result)
                st.markdown(formatted_result, unsafe_allow_html=True)
            st.session_state.processing = False
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.session_state.processing = False

if __name__ == "__main__":
    main()