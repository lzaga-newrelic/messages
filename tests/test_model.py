import pytest
from asynctest import CoroutineMock
from unittest.mock import MagicMock, AsyncMock

from messages import model


# Integration test
@pytest.mark.asyncio
async def test_go():
    from messages.model import MessagesModel
    res = await MessagesModel.go()
    assert isinstance(res, dict) is True


@pytest.fixture
def engine_mock():
    model.engine = CoroutineMock()
    model.engine.acquire = MagicMock()
    return model.engine


@pytest.mark.asyncio
async def test_add(event_loop, engine_mock):
    message = 'test'

    request_mock = AsyncMock()
    request_mock.__aenter__.return_value = request_mock

    engine_mock.acquire.return_value = request_mock

    await model.MessagesModel.add(message)
    assert request_mock.execute.call_count == 2
