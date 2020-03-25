from aiogram.dispatcher import Dispatcher


async def close_redis_connections(dispatcher: Dispatcher):
    for conn in dispatcher["app"]["redis"].values():
        try:
            await conn.close()
        except TypeError:
            conn.close()
