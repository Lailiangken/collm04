import json
import os
from autogen_agentchat.agents import AssistantAgent
from .tools_manager import ToolsManager

def load_agents_from_directory(agents_dir, model_client, agent_class=AssistantAgent):
    tools_manager = ToolsManager()
    agents = []
    
    for filename in os.listdir(agents_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(agents_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                agent_info = json.load(f)
                
                # JSONからツール情報を取得
                tools = []
                if "tools" in agent_info:
                    for tool_name in agent_info["tools"]:
                        tool = tools_manager.get_tool(tool_name)
                        if tool:
                            tools.append(tool)
                
                agent = agent_class(
                    name=agent_info['name'],
                    model_client=model_client,
                    system_message=agent_info['system_message'],
                    tools=tools if tools else None
                )
                agents.append(agent)
    return agents