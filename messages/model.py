import sqlalchemy as sa
from aiomysql.sa import create_engine
from structlog import get_logger

DB_NAME = 'onboarding'
PORT = 3306
PASS = ''
USER = 'root'
HOST = 'localhost'

log = get_logger()
log = log.bind(user=USER)
metadata = sa.MetaData()

messages_table = sa.Table('messages', metadata, sa.Column('id', sa.Integer, primary_key=True),
                          sa.Column('message', sa.String(255)))


class MessagesModel:
    def __init__(self):
        self.__engine = None

    async def get_engine(self):
        if self.__engine is None:
            self.__engine = await create_engine(user=USER, db=DB_NAME, port=PORT, host=HOST, password=PASS)

        return self.__engine

    async def add(self, message):
        engine_instance = await self.get_engine()
        async with engine_instance.acquire() as conn:
            await conn.execute(messages_table.insert().values(message=message))
            await conn.execute('commit')

            log.info("message was added to db", message=message)

    async def get(self):
        engine_instance = await self.get_engine()
        dicts = {}
        async with engine_instance.acquire() as conn:
            res = await conn.execute(messages_table.select())
            for row in (await res.fetchall()):
                log.info("message was pulled out of db", row=row.id)
                dicts[row.id] = row.message
        return dicts
