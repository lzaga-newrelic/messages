import pytest
from asynctest import CoroutineMock, MagicMock
from unittest.mock import MagicMock, AsyncMock, Mock

from messages.model import MessagesModel


# Integration test
@pytest.mark.asyncio
async def test_get():
    res = await MessagesModel().get()
    assert isinstance(res, dict) is True


@pytest.fixture
def engine_mock():
    get_engine = CoroutineMock()
    get_engine.acquire = MagicMock()
    get_engine.return_value = get_engine

    return get_engine


@pytest.mark.asyncio
async def test_add(event_loop, engine_mock):
    message = 'test'
    model = MessagesModel()

    request_mock = AsyncMock()
    request_mock.__aenter__.return_value = request_mock
    engine_mock.acquire.return_value = request_mock

    model.get_engine = engine_mock

    await model.add(message)
    assert request_mock.execute.call_count == 2
