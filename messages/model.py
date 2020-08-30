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

messages_table = sa.Table('messages', metadata, sa.Column('id', sa.Integer, primary_key=True), sa.Column('message', sa.String(255)))

engine = None


async def get_engine():
    global engine
    if engine is None:
        engine = await create_engine(user=USER, db=DB_NAME, port=PORT, host=HOST, password=PASS)

    return engine


class MessagesModel:
    @classmethod
    async def add(cls, message):
        engine_instance = await get_engine()
        async with engine_instance.acquire() as conn:
            await conn.execute(messages_table.insert().values(message=message))
            await conn.execute('commit')

            log.info("message was added to db", message=message)

    @classmethod
    async def go(cls):
        engine_instance = await get_engine()
        dicts = {}
        async with engine_instance.acquire() as conn:
            res = await conn.execute(messages_table.select())
            for row in (await res.fetchall()):
                log.info("message was pulled out of db", row=row.id)
                dicts[row.id] = row.message
        return dicts
