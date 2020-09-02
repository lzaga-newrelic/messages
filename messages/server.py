from signipy.http.server import BaseServer

from messages.pubsub.pusub_messages import MessagesSubscriptionHandler
from messages.handlers.messages import MessagesHandler


class MessagesServer(BaseServer):
    def __init__(self):
        super().__init__()
        self.dependencies.update({})

    def add_pubsub_handlers(self):
        self.add_pubsub_handler(
            "messages",
            "messages_subscription",
            MessagesSubscriptionHandler,
            "errors"
        )

        return super().add_pubsub_handlers()

    def add_routes(self):
        self.add_route(r'/messages', MessagesHandler)

        return super().add_routes()
