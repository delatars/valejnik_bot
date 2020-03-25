import logging
from aiogram.dispatcher import Dispatcher

from valejnik_bot.setup_handlers import setup_handlers
from .on_startup_actions import (
    set_webhook_if_mode_webhook,
    create_redis_connections,
    set_dispatcher_storage,
    setup_polls_objects,
    init_meme_queue,
)


logger = logging.getLogger("valejnik.startup_actions")


async def on_startup(dispatcher: Dispatcher):
    dispatcher["app"] = app = {}

    await create_redis_connections(dispatcher)
    set_dispatcher_storage(dispatcher)
    setup_polls_objects(dispatcher)
    await init_meme_queue(dispatcher)
    await set_webhook_if_mode_webhook(dispatcher)
    setup_handlers(dispatcher)

    indent = "\n" + "\t"
    logger.info(f"Setup app: {indent}{indent.join((f'{k} -> {v}' for k,v in app.items()))}")




