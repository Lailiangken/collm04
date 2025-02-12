import streamlit as st
import logging
from .main.render_chat import render_chat_section
from autogen_functions.group_chat.group_chat import run_group_chat
from ..utils.formatters import format_task_result

def render_main_content(selected_group):
    st.title("Group Chat Assistant")
    st.markdown("グループチャットでは、SelectorGroupChatまたはMagenticOneGroupChatを選択できます。")
    
    chat_type, use_web_surfer, use_code_executor = render_chat_section()
    task = st.text_area("議論するタスクや話題を入力してください:", height=200)

    if 'processing' not in st.session_state:
        st.session_state.processing = False

    button_text = "処理中..." if st.session_state.processing else "実行"
    
    formatted_result,last_result=handle_chat_execution(
        button_text, 
        task, 
        selected_group,
        use_web_surfer,
        use_code_executor, 
        chat_type
    )

    chat_info = {
        "chat_type": chat_type,
        "use_web_surfer": use_web_surfer,
        "use_code_executor": use_code_executor,
        "selected_group": selected_group,
        "task": task
    }
    return formatted_result, chat_info ,last_result

def handle_chat_execution(button_text, task, selected_group,use_web_surfer,use_code_executor, chat_type):
    formatted_result =""
    last_result = ""
    if st.button(button_text, disabled=st.session_state.processing) and task:
        try:
            st.session_state.processing = True
            with st.spinner("処理中..."):
                logger = logging.getLogger(__name__)
                logger.info("タスクを実行中: %s", task)
                task_result = run_group_chat(
                    task, 
                    use_web_surfer=use_web_surfer,
                    use_code_executor=use_code_executor,
                    group_name=selected_group, 
                    chat_type=chat_type
                )
                formatted_result, last_result = format_task_result(task_result)
                st.markdown(last_result, unsafe_allow_html=True)
                st.markdown(formatted_result, unsafe_allow_html=True)
            st.session_state.processing = False
            logger.info("タスクが完了しました")
        except Exception as e:
            logger.error("エラーが発生しました: %s", e)
            st.error("エラーが発生しました。詳細はログを確認してください。")
        finally:
            st.session_state.processing = False
    return formatted_result, last_result
