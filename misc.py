# -*- coding: utf-8 -*-
import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

from aiogram.contrib.fsm_storage.redis import RedisStorage2

import config
from custom_filters import ChatTypeFilter


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout
)
logger = logging.getLogger("valejnik.misc")

bot = Bot(token=config.TELEGRAM_BOT_API_KEY, proxy=config.PROXY_URL, proxy_auth=config.PROXY_AUTH)
logger.info(f"Initialize bot: {bot}")


RedisPoolDispatcher = RedisStorage2(host=config.REDIS_SERVER, port=config.REDIS_PORT, db=0, pool_size=20)
RedisPoolMemes = RedisStorage2(host=config.REDIS_SERVER, port=config.REDIS_PORT, db=1, pool_size=20)

dispatcher = Dispatcher(bot, storage=RedisPoolDispatcher)
logger.info(f"Initialize dispatcher: {dispatcher}")

# - Register custom filter
dispatcher.filters_factory.bind(ChatTypeFilter, event_handlers=[dispatcher.message_handlers])

executor = Executor(dispatcher)
logger.info(f"Initialize executor: {executor}")
