import logging
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_core.logging import LLMCallEvent
from autogen_core import EVENT_LOGGER_NAME

# ログの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(EVENT_LOGGER_NAME)

def log_event(messages, response, prompt_tokens=0, completion_tokens=0):
    """ログを記録するための共通メソッド"""
    event = LLMCallEvent(
        messages=messages,
        response=response,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
    logger.info(event)

class LoggingAssistantAgent(AssistantAgent):
    async def on_messages(self, messages, cancellation_token):
        for message in messages:
            log_event(messages, message.content)  # 外部メソッドを使用
            
        response = await super().on_messages(messages, cancellation_token)
        
        log_event(messages, response.content)  # 外部メソッドを使用
        return response

class LoggingUserProxyAgent(UserProxyAgent):
    async def on_messages(self, messages, cancellation_token):
        for message in messages:
            log_event(messages, message.content)  # 外部メソッドを使用
            
        response = await super().on_messages(messages, cancellation_token)
        
        log_event(messages, response.content)  # 外部メソッドを使用
        return response
