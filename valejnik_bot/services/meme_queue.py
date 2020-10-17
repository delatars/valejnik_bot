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
    DISABLE_NOTIFICATION = True
    ON_ERROR_TIMEOUT = 10 * 60

    def __init__(self, dispatcher: Dispatcher, *args, **kwargs):
        self.redis = dispatcher["app"]["redis"]["polls_storage"]
        self.dispatcher = dispatcher
        self.sends_post_to = dispatcher["config"]["bot"]["posts"]["post_channel_id"]
        super().__init__(*args, **kwargs)

    def redis_generate_key(self, *parts):
        return ':'.join((self.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    async def start_posting(self, timeout=1):
        """ Get meme from queue and post it.

        :type timeout: int: time (in minutes) to sleep between next post
        """
        # start delay
        await asyncio.sleep(5)

        while 1:
            message = await self.get()
            image_id = message.reply_to_message.photo[1].file_id
            redis_key = self.redis_generate_key(image_id)

            while 1:
                try:
                    logger.info(f"Send item: {image_id} :to channel: {self.sends_post_to}")
                    await self.dispatcher.bot.send_photo(self.sends_post_to, image_id,
                                                         disable_notification=self.DISABLE_NOTIFICATION)
                except NeedAdministratorRightsInTheChannel:
                    logger.warning(f"AdministratorRightsError: Need rights escalation for channel:"
                                   f" {self.sends_post_to}")
                    await self.dispatcher.bot.send_message(message.chat.id,
                                                           f"Мне нужны права администратора на отправку сообщений,"
                                                           f" чтобы отправить пост в канал: {self.sends_post_to}")
                except TelegramAPIError as ex:
                    logger.error(f"TelegramApiError: {str(ex)}")
                    logger.info(f"Standby queue for {self.ON_ERROR_TIMEOUT} seconds")
                    await asyncio.sleep(self.ON_ERROR_TIMEOUT)
                except Exception as ex:
                    logger.error(f"UnknownError: something went wrong: {str(ex)}")
                    await asyncio.sleep(self.ON_ERROR_TIMEOUT)
                else:
                    await self.remove_from_redis(redis_key)
                    await asyncio.sleep(timeout*60)
                    break

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
        return message

    async def remove_from_redis(self, key):
        await self.redis.delete(key)


if __name__ == '__main__':
    pass
