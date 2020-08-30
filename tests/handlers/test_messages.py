import pytest
import json
from tornado import web

import messages.handlers.messages as MessagesHandler
import messages.main as MainHandler


@pytest.fixture
def app():
    return web.Application([
        (r"/", MainHandler),
        (r"/messages", MessagesHandler)]
    )


def get_url(path=''):
    url = 'http://localhost:3000/' + path
    return url


@pytest.mark.asyncio
async def test_http_server(http_client):
    url = get_url()
    resp = await http_client.fetch(url)
    assert resp.code == 200
    assert resp.body == b"Hello, world"


@pytest.mark.asyncio
async def test_get_messages(http_client):
    url = get_url('messages')
    resp = await http_client.fetch(url)
    assert resp.code == 200
    assert isinstance(json.loads(resp.body), dict) is True


@pytest.mark.asyncio
async def test_get_messages(http_client, event_loop):
    url = get_url('messages')

    post_data = {'message': 'test'}
    body = json.dumps(post_data)
    resp = await http_client.fetch(url, method='POST', headers=None, body=body)

    assert resp.code == 200
