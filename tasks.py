# -*- coding: utf-8 -*-
import asyncio

import config
from misc import bot
from services.meme_queue import AsyncQueue


loop = asyncio.get_event_loop()

# - Initialize queue
MemeQueue = AsyncQueue(100)
# logger.info(f"Initialize MemeQueue: {MemeQueue}")

# Create tasks
task1 = loop.create_task(MemeQueue.load_queue())
task2 = loop.create_task(MemeQueue.start_posting(bot, config.TIME_BETWEEN_POSTS))


def initialize_tasks():
    return loop


if __name__ == '__main__':
    pass
