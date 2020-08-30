from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
import asyncio
import uvloop
from structlog import get_logger

from messages.handlers.messages import MessagesHandler

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
log = get_logger()


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/messages", MessagesHandler)
    ])


def main():
    app = make_app()
    app.listen(3000)
    log.info("Server is running.....")
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
