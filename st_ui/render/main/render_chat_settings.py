import streamlit as st

def render_chat_section():
    chat_type = st.selectbox(
        "チャットタイプを選択してください:",
        ["selector", "magentic"],
        format_func=lambda x: "Selector Chat" if x == "selector" else "Magentic-One Chat"
    )
    if chat_type == "selector":
        st.info("Selector Chat: グループチャットのつぎの発話者は、メンバーのうち最も適切である(とLLMが判断した)メンバーになります。")
    else:
        st.info("Magentic-One Chat: Orchestratorが主導して、タスクを小さなステップに分解し、適切なエージェントに割り当てて実行します。")
    
    use_web_surfer = st.checkbox(
        "Web Surferを使用する", 
        help="Web検索機能を有効にします。インターネットからの情報収集が必要な場合に使用してください。"
    )
    
    use_code_executor = st.checkbox(
        "Code Executorを使用する",
        help="Pythonコードの実行機能を有効にします。実行環境は専用のDockerコンテナ上です。コードの実行が必要な場合に使用してください。"
    )

    return chat_type, use_web_surfer, use_code_executor