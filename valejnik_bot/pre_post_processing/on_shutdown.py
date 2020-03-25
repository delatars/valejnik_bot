from aiogram.dispatcher import Dispatcher

from .on_shutdown_actions import close_redis_connections


async def on_shutdown(dispatcher: Dispatcher):
    await close_redis_connections(dispatcher)
