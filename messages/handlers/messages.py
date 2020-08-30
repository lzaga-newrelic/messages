import json
from tornado.web import RequestHandler

from messages.model import MessagesModel


class MessagesHandler(RequestHandler):
    async def get(self):
        res = await MessagesModel.go()
        self.write(json.dumps(res))
        await self.finish()

    async def post(self):
        message = json.loads(self.request.body)['message']
        await MessagesModel.add(message)
