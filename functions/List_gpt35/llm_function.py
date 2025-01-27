from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from pathlib import Path
import pandas as pd
import json
import os

class LLMFunction:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0
        )
        self.base_prompt = "あなたはPythonプログラマーとして回答します。サブクエリや質問を分解する場合でも、必ず1つのリストにまとめて出力してください。"
        self.module_dir = Path(os.path.dirname(__file__))
        self.roles = self._load_roles()
        self.system_prompt = self._load_prompt()
        
    def _load_roles(self) -> list:
        roles_path = self.module_dir / "prompts/roles.json"
        with open(roles_path) as f:
            return json.load(f)["roles"]
        
    def _load_prompt(self) -> str:
        prompts_path = self.module_dir / "prompts/prompts.csv"
        examples_path = self.module_dir / "prompts/examples.csv"
        
        df_prompts = pd.read_csv(prompts_path)
        instructions = [f"{row['id']}. {row['instruction']}" for _, row in df_prompts.iterrows()]
        
        df_examples = pd.read_csv(examples_path)
        examples = [f"{row['content']}" for _, row in df_examples.iterrows()]
        
        full_prompt = f"""{self.base_prompt}
以下の形式で厳密に回答してください:
{chr(10).join(instructions)}

重要: 複数のリストではなく、必ず1つのリストにまとめて出力してください。
出力例:
{chr(10).join(examples)}"""
        
        return full_prompt

    def __call__(self, user_input: str) -> str:
        messages = [SystemMessage(content=self.system_prompt)]
        
        for role in self.roles:
            if role['role'] == 'system':
                messages.append(SystemMessage(content=role['content']))
            elif role['role'] == 'assistant':
                messages.append(AIMessage(content=role['content']))
            elif role['role'] == 'user':
                messages.append(HumanMessage(content=role['content']))
                
        messages.append(HumanMessage(content=user_input))
        
        response = self.llm(messages)
        return response.content