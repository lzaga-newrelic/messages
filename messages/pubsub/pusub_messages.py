import json
from signipy.gcloud.pubsub import Message, SubscriptionHandler
from structlog import get_logger

from messages.model import MessagesModel


class MessagesSubscriptionHandler(SubscriptionHandler):
    def __init__(self):
        self.logger = get_logger('.'.join((self.__module__, self.__class__.__name__)))
        self.model = MessagesModel()

    async def handle(self, message: Message):
        data = message.data.decode("utf-8")

        await self.model.add(data)
        self.logger.info('Received ans saved message:', data=data)
