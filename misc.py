# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

from tmp.config import TELEGRAM_BOT_API_KEY, PROXY_URL, PROXY_AUTH, TIME_BETWEEN_POSTS
from custom_filters import ChatTypeFilter
from services.meme_queue import AsyncQueue


# - Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_API_KEY, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dispatcher = Dispatcher(bot)

# - Register custom filter
dispatcher.filters_factory.bind(ChatTypeFilter, event_handlers=[dispatcher.message_handlers])

# - Initialize queue
MemeQueue = AsyncQueue(100)

loop = asyncio.get_event_loop()
task = loop.create_task(MemeQueue.start_posting(TIME_BETWEEN_POSTS))

executor = Executor(dispatcher)
