from autogen_functions.group_chat.group_chat_043 import run_group_chat

def main():
    task = """
    新しいPythonウェブアプリケーションの設計について議論を行います。

    要件:
    1. FastAPIを使用したRESTful API
    2. PostgreSQLデータベース連携
    3. JWT認証システム
    4. OpenAPI仕様に準拠したAPI文書
    
    アーキテクチャ設計から実装方針まで検討してください。
    議論が完了したら「終了」と発言してください。
    """
    
    result = run_group_chat(task)
    print(result)

if __name__ == "__main__":
    main()
