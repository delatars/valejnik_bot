# -*- coding: utf-8 -*-
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import TELEGRAM_BOT_API_KEY, PROXY_URL, PROXY_AUTH, TIME_BETWEEN_POSTS
from custom_filters import ChatTypeFilter
from services.meme_queue import AsyncQueue


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout
)
logger = logging.getLogger("valejnik.misc")


bot = Bot(token=TELEGRAM_BOT_API_KEY, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
logger.info(f"Initialize bot: {bot}")

storage = MemoryStorage()
# redis = RedisStorage2(host="172.17.0.3", db=0)
dispatcher = Dispatcher(bot, storage=storage)
logger.info(f"Initialize dispatcher: {dispatcher}")

# - Register custom filter
dispatcher.filters_factory.bind(ChatTypeFilter, event_handlers=[dispatcher.message_handlers])

# - Initialize queue
MemeQueue = AsyncQueue(100)
logger.info(f"Initialize MemeQueue: {MemeQueue}")

loop = asyncio.get_event_loop()
task = loop.create_task(MemeQueue.start_posting(bot, TIME_BETWEEN_POSTS))

executor = Executor(dispatcher, loop=loop)
logger.info(f"Initialize executor: {executor}")
