import logging
import json
import asyncio
from aiogram.utils.exceptions import NeedAdministratorRightsInTheChannel, TelegramAPIError
from aiogram import Dispatcher, types
from time import time


__all__ = ["AsyncQueue"]


logger = logging.getLogger("valejnik.services.meme_queue")


class AsyncQueue(asyncio.Queue):

    REDIS_KEY_PREFIX = "queue"
    SEND_POSTS_TO = "@Valejnick"
    DISABLE_NOTIFICATION = True
    ON_ERROR_TIMEOUT = 10 * 60

    def __init__(self, dispatcher: Dispatcher, *args, **kwargs):
        self.redis = dispatcher["app"]["redis"]["polls_storage"]
        self.dispatcher = dispatcher
        super().__init__(*args, **kwargs)

    def redis_generate_key(self, *parts):
        return ':'.join((self.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    async def start_posting(self, timeout=1):
        """ Get meme from queue and post it.

        :type timeout: int: time (in minutes) to sleep between next post
        """

        while 1:
            message = await self.get()
            try:
                await self.dispatcher.bot.send_photo(self.SEND_POSTS_TO, message.reply_to_message.photo[1].file_id,
                                                     disable_notification=self.DISABLE_NOTIFICATION)
            except NeedAdministratorRightsInTheChannel:
                logger.warning(f"AdministratorRightsError: Need rights escalation for channel: {self.SEND_POSTS_TO}")
                await self.dispatcher.bot.send_message(message.chat.id,
                                                       f"Мне нужны права администратора на отправку сообщений,"
                                                       f" чтобы отправить пост в канал: {self.SEND_POSTS_TO}")
            except TelegramAPIError:
                logger.error(f"TelegramApiError: standby queue for {self.ON_ERROR_TIMEOUT} seconds")
                await asyncio.sleep(self.ON_ERROR_TIMEOUT)
            except Exception as ex:
                logger.error(f"UnknownError: something went wrong: {str(ex)}")
                await asyncio.sleep(self.ON_ERROR_TIMEOUT)
            else:
                await asyncio.sleep(timeout*60)

    async def load_queue(self):
        logger.info("Loading queue...")
        pattern = self.redis_generate_key("*")
        keys = [(await self.redis.hget(key, "timestamp"), key) for key in await self.redis.keys(pattern)]
        if keys:
            keys.sort()
            for item in keys:
                logger.info(f" -> Load: {item[0]} -> {item[1]}")
                message = await self.redis.hget(item[1], "message")
                await super().put(types.Message.to_object(json.loads(message)))
        else:
            logger.info(" -> Queue is empty.")

    async def put(self, message: types.Message):
        key = self.redis_generate_key(message.reply_to_message.photo[1].file_id)
        await self.redis.hset(key, "timestamp", time())
        await self.redis.hset(key, "message", message.as_json())
        await super().put(message)

    async def get(self) -> types.Message:
        message = await super().get()
        key = self.redis_generate_key(message.reply_to_message.photo[1].file_id)
        await self.redis.delete(key)
        return message


if __name__ == '__main__':
    pass
