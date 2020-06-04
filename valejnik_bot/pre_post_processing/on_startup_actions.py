import aioredis
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Dispatcher

from valejnik_bot.services.polls import GroupMemePoll, UsersMemePoll
from valejnik_bot.services.meme_queue import AsyncQueue


async def set_webhook_if_mode_webhook(dispatcher: Dispatcher):
    bot = dispatcher.bot
    api_config = dispatcher["config"]["general"]["api"]
    url = api_config["webhook"]["url"]
    cert = api_config["webhook"]["cert"]

    # Get current webhook status
    webhook = await bot.get_webhook_info()

    if url:
        if webhook.url != url:
            if not webhook.url:
                await bot.delete_webhook()

            if cert:
                with open(cert, 'rb') as cert_file:
                    await bot.set_webhook(url, certificate=cert_file)
            else:
                await bot.set_webhook(url)
    elif webhook.url:
        await bot.delete_webhook()


async def create_redis_connections(dispatcher: Dispatcher):
    app = dispatcher["app"]
    redis_host = dispatcher["config"]["general"]["redis"]["host"]
    redis_port = dispatcher["config"]["general"]["redis"]["port"]

    fsm_storage = RedisStorage2(host=redis_host, port=redis_port, db=0, pool_size=20)
    polls_storage = await aioredis.create_redis_pool((redis_host, redis_port), db=1, maxsize=20)

    app["redis"] = {"fsm_storage": fsm_storage, "polls_storage": polls_storage}


def set_dispatcher_storage(dispatcher: Dispatcher):
    app = dispatcher["app"]
    dispatcher.storage = app["redis"]["fsm_storage"]


def setup_polls_objects(dispatcher: Dispatcher):
    app = dispatcher["app"]
    app["polls"] = {}
    app["polls"]["group"] = GroupMemePoll(app["redis"]["polls_storage"])
    app["polls"]["users"] = UsersMemePoll(app["redis"]["polls_storage"])


async def init_meme_queue(dispatcher: Dispatcher):
    app = dispatcher["app"]
    app["queue"] = meme_queue = AsyncQueue(dispatcher, maxsize=100)
    await meme_queue.load_queue()
    dispatcher.loop.create_task(meme_queue.start_posting(
        timeout=dispatcher["config"]["bot"]["posts"]["time_between_posts"])
    )
