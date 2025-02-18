import logging
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_core import EVENT_LOGGER_NAME

# TRACEログの設定
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(EVENT_LOGGER_NAME)

def log_event(messages, response_content):
    """ログを記録するための共通メソッド"""
    # メッセージの内容をログに記録
    for message in messages:
        logger.info(f"[LoggingAgents] Message from {message.source}: {message.content}")
    logger.info(f"[LoggingAgents] Response: {response_content}")

class LoggingAssistantAgent(AssistantAgent):
    async def on_messages(self, messages, cancellation_token):
        response = await super().on_messages(messages, cancellation_token)
        log_event(messages, response.content)
        return response

class LoggingUserProxyAgent(UserProxyAgent):
    async def on_messages(self, messages, cancellation_token):
        response = await super().on_messages(messages, cancellation_token)
        log_event(messages, response.content)
        return response