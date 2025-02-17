import pytest
import asyncio
from unittest.mock import MagicMock
from sample2 import ChatRunner

@pytest.mark.asyncio
async def test_chat_runner():
    # モックの準備
    mock_chat_area = MagicMock()
    chat_runner = ChatRunner(chat_area=mock_chat_area)
    
    # チャット実行
    result = await chat_runner.run_chat(task="Test message")
    
    # アサーション
    assert isinstance(result, str)
    assert mock_chat_area.markdown.called

@pytest.mark.asyncio
async def test_chat_runner_with_different_chat_type():
    mock_chat_area = MagicMock()
    chat_runner = ChatRunner(chat_area=mock_chat_area)
    
    result = await chat_runner.run_chat(
        task="Test message",
        chat_type="selector"
    )
    
    assert isinstance(result, str)
