import logging
import streamlit as st
import json
from pathlib import Path
from autogen_functions.group_chat.group_chat_043 import run_group_chat

# Custom Streamlit logging handler
class StreamlitHandler(logging.Handler):
    def __init__(self, log_area):
        super().__init__()
        self.log_area = log_area
        self.log_data = ""
        self.log_area=log_area.empty()

    def emit(self, record):
        log_entry = self.format(record)
        self.log_data += log_entry + "\n\n"
        self.log_area.markdown(f"\n{self.log_data}\n")


def create_new_agent_config(agent_name,group_name):
    config_path = Path("autogen_functions/group_chat")/ group_name /"agents"/ f"{agent_name}_config.json"
    if config_path.exists():
        raise FileExistsError(f"エージェント '{agent_name}' は既に存在します")
    
    default_config = {
        "name": agent_name,
        "system_message": "新しいエージェントのシステムメッセージをここに入力してください"
    }
    
    save_agent_config(config_path, default_config)
    return config_path
def create_new_group(group_name):
    template_dir = Path("template/agents")
    new_group_dir = Path("autogen_functions/group_chat") / group_name / "agents"
    
    if new_group_dir.exists():
        raise FileExistsError(f"グループ '{group_name}' は既に存在します")
    
    # フォルダツリーを作成
    new_group_dir.parent.mkdir(exist_ok=True)
    # テンプレートフォルダを新しいグループフォルダにコピー
    import shutil
    shutil.copytree(template_dir, new_group_dir)
    return new_group_dir

def delete_group(group_name):
    import shutil
    group_dir = Path("autogen_functions/group_chat") / group_name
    
    if not group_dir.exists():
        return False
        
    try:
        shutil.rmtree(group_dir)
        return True
    except Exception:
        return False

def get_available_groups():
    group_dir = Path("autogen_functions/group_chat")
    return [d.name for d in group_dir.iterdir() 
            if d.is_dir() 
            and d.name != "template" 
            and not d.name.startswith("__")]

def load_agent_configs(group_name):
    agent_dir = Path("autogen_functions/group_chat") / group_name / "agents"
    configs = {}
    for config_file in agent_dir.glob("*_config.json"):
        with open(config_file, "r") as f:
            configs[config_file.stem] = {
                "path": config_file,
                "data": json.load(f)
            }
    return configs

def save_agent_config(file_path, config):
    with open(file_path, "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
def delete_agent_config(file_path):
    path = Path(file_path)
    if path.exists():
        path.unlink()
        return True
    return False

def format_task_result(task_result):
    md_output = "# 議論の結果\n\n"
    for message in task_result.messages:
        md_output += f"## {message.source.capitalize()}\n"
        md_output += f"{message.content}\n\n"
    return md_output

def main():
    st.title("Group Chat Assistant")

    with st.sidebar:
        st.header("グループ設定")
        # グループ選択
        available_groups = get_available_groups()
        if not available_groups:
            st.warning("利用可能なグループがありません")
            return        
        # グループ追加UI

        selected_group = st.selectbox(
            "読み込むグループを選択",
            available_groups,
            index=available_groups.index("Agents") if "Agents" in available_groups else 0
        )



        with st.expander("グループ追加/削除", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                new_group_name = st.text_input("新規グループ名", key="new_group_input", 
                                             label_visibility="collapsed", 
                                             placeholder="新規グループ名を入力")
                selected_group = st.selectbox(
                    "削除するグループを選択",
                    available_groups,
                    label_visibility="collapsed", 
                    index=available_groups.index("Agents") if "Agents" in available_groups else 0,
                    placeholder="削除するグループを選択"
                )
            with col2:
                if st.button("グループを追加", key="add_group"):
                    if new_group_name:
                        try:
                            create_new_group(new_group_name)
                            st.success(f"グループ '{new_group_name}' を作成しました")
                            st.rerun()
                        except FileExistsError as e:
                            st.error(str(e))
                    else:
                        st.error("グループ名を入力してください")
                if selected_group != "Default":  # Agentsグループは削除できないように保護
                    if st.button("グループを削除", key="delete_group"):
                        if delete_group(selected_group):
                            st.success(f"グループ '{selected_group}' を削除しました")
                            st.rerun()
                        else:
                            st.error("グループの削除に失敗しました")



 
        st.header("エージェント設定")
        
        # 既存のエージェント設定部分
        agent_configs = load_agent_configs(selected_group)
        if agent_configs:
            agent_tabs = st.tabs(list(agent_configs.keys()))
            for tab, (agent_name, config_data) in zip(agent_tabs, agent_configs.items()):
                with tab:
                    new_name = st.text_input(
                        "Name", 
                        config_data["data"]["name"],
                        key=f"{agent_name}_name"
                    )
                    new_system_message = st.text_area(
                        "System Message", 
                        config_data["data"]["system_message"],
                        height=200,
                        key=f"{agent_name}_system_message"
                    )
                    col1, col2, col3 = st.columns([1, 1,2])
                    with col1:
                        if st.button("設定を保存", key=f"{agent_name}_save"):
                            updated_config = {
                                "name": new_name,
                                "system_message": new_system_message
                            }
                            save_agent_config(config_data["path"], updated_config)
                            st.success(f"{agent_name}の設定を保存しました")
                    with col2:
                        if st.button("Agentを削除", key=f"{agent_name}_delete"):
                            if delete_agent_config(config_data["path"]):
                                st.success(f"{agent_name}を削除しました")
                                st.rerun()
                            else:
                                st.error("削除に失敗しました")
                    with col3:
                        st.markdown("")
        else:
            st.info("このグループにはエージェントが存在しません。新しいエージェントを追加してください。")        
            with st.expander("エージェント追加", expanded=True):
                col1, col2 = st.columns([2, 1])
            with col1:
                new_agent_name = st.text_input("新規エージェント名", key="new_agent_input", label_visibility="collapsed", placeholder="エージェント名を入力")
            with col2:
           
                if st.button("Agentを追加", key="add_agent"):
                    if new_agent_name:
                        try:
                            create_new_agent_config(new_agent_name,selected_group)
                            st.success(f"エージェント '{new_agent_name}' を作成しました")
                            st.rerun()
                        except FileExistsError as e:
                            st.error(str(e))
                    else:
                        st.error("エージェント名を入力してください")                     
                         # ログの表示をサイドバーの下に追加
        st.header("ログ")
        
        with st.expander("ログを表示/非表示", expanded=False):
            log_display = st.container()
            streamlit_handler = StreamlitHandler(log_display)
            streamlit_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(streamlit_handler)

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
                logger = logging.getLogger(__name__)
                logger.info("タスクを実行中: %s", task)
                task_result = run_group_chat(task, chat_mode=chat_mode)
                formatted_result = format_task_result(task_result)
                st.markdown(formatted_result, unsafe_allow_html=True)
            st.session_state.processing = False
            logger.info("タスクが完了しました")
        except Exception as e:
            logger.error("エラーが発生しました: %s", e)
            st.error("エラーが発生しました。詳細はログを確認してください。")
        finally:
            st.session_state.processing = False

if __name__ == "__main__":
    main()


