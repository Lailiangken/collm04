from autogen_functions.tools_manager import ToolsManager

# ToolsManagerのインスタンス化
tools_manager = ToolsManager()

# 利用可能な関数の一覧を取得
available_functions = tools_manager.list_available_functions()
print("Available functions:", available_functions)

# 特定の関数のツール情報を取得
tool = tools_manager.get_tool("goal_setting_info")
if tool:
    print(f"Tool name: {tool.name}")
    print(f"Tool description: {tool.description}")
