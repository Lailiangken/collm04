from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

# Create the agents.
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
assistant = AssistantAgent("assistant", model_client=model_client)

# Create the team setting a maximum number of turns to 1.
team = RoundRobinGroupChat([assistant], max_turns=1)

async def main():
    task = "あなたはコールセンターのオペレーターです。ユーザがいると仮定して、その職位、メールアドレス、電話番号を聞き出してください。"
    while True:
        stream = team.run_stream(task=task)
        await Console(stream)
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.lower().strip() == "exit":
            break

if __name__ == "__main__":
    asyncio.run(main())     