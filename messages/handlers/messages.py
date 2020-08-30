import json
from tornado.web import RequestHandler

from messages.model import MessagesModel


class MessagesHandler(RequestHandler):
    model = MessagesModel()

    async def get(self):
        res = await self.model.get()
        await self.finish(json.dumps(res))

    async def post(self):
        message = json.loads(self.request.body)['message']
        await self.model.add(message)
