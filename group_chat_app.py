import streamlit as st
from autogen_functions.group_chat.group_chat_043 import run_group_chat

def main():
    st.title("Group Chat Assistant")

    task = st.text_area("議論するタスクや話題を入力してください:", height=200)

    if 'processing' not in st.session_state:
        st.session_state.processing = False

    button_text = "処理中..." if st.session_state.processing else "実行"
    if st.button(button_text, disabled=st.session_state.processing) and task:
        try:
            st.session_state.processing = True
            with st.spinner("処理中..."):
                result = run_group_chat(task)
                st.markdown("### 議論の結果")
                st.markdown(result, unsafe_allow_html=True)
            st.session_state.processing = False
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.session_state.processing = False

if __name__ == "__main__":
    main()
