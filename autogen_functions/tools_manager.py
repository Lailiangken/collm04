import os
import inspect
import importlib.util
from typing import List, Dict, Optional
from autogen_core.tools import FunctionTool

class ToolsManager:
    def __init__(self, tools_dir: str = "tools"):
        self.tools_dir = tools_dir
        self.function_tools: Dict[str, FunctionTool] = {}
        self._load_all_tools()

    def _load_all_tools(self) -> None:
        """toolsディレクトリから全ての関数を読み込みFunctionToolとして保持"""
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and not file.startswith('__'):
                module_path = os.path.join(self.tools_dir, file)
                module_name = file[:-3]
                
                # モジュールを動的にロード
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # モジュール内の全ての関数を取得
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        tool = FunctionTool(
                            obj,
                            description=obj.__doc__ or f"Function {name} from {module_name}"
                        )
                        self.function_tools[name] = tool

    def list_available_functions(self) -> List[str]:
        """利用可能な関数名のリストを返す"""
        return list(self.function_tools.keys())

    def get_tool(self, function_name: str) -> Optional[FunctionTool]:
        """指定された関数名のFunctionToolを返す"""
        return self.function_tools.get(function_name)
