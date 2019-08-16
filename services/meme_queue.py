# -*- coding: utf-8 -*-
import logging
import json
import asyncio
from aiogram.utils.exceptions import NeedAdministratorRightsInTheChannel
from aiogram import Bot, types
from utils import RedisConnector
from time import time


__all__ = ["AsyncQueue"]


logger = logging.getLogger("valejnik.services.meme_queue")


class AsyncQueue(asyncio.Queue, RedisConnector):

    SEND_POSTS_TO = "@Valejnick"
    DISABLE_NOTIFICATION = True
    REDIS_DB = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start_posting(self, control: Bot, timeout=1):
        """ Get meme from queue and post it.

        :type timeout: int: time (in minutes) to sleep between next post
        """
        while 1:
            message = await self.get()
            try:
                await control.send_photo(self.SEND_POSTS_TO, message.reply_to_message.photo[1].file_id,
                                         disable_notification=self.DISABLE_NOTIFICATION)
            except NeedAdministratorRightsInTheChannel:
                await control.send_message(message.chat.id, f"Мне нужны права администратора на отправку сообщений,"
                                                            f" чтобы отправить пост в канал: {self.SEND_POSTS_TO}")
            else:
                await asyncio.sleep(timeout*60)

    async def load_queue(self):
        logger.info("Loading queue...")
        pattern = self.redis_generate_key("queue", "*")
        keys = [(await self.redis_hget(key, "timestamp"), key) for key in await self.redis_keys(pattern)]
        if keys:
            keys.sort()
            for item in keys:
                logger.info(f" -> Load: {item[0]} -> {item[1]}")
                message = await self.redis_hget(item[1], "message")
                await super().put(types.Message.to_object(json.loads(message)))
        else:
            logger.info(" -> Queue is empty.")

    async def put(self, message: types.Message):
        key = self.redis_generate_key("queue", message.reply_to_message.photo[1].file_id)
        await self.redis_hset(key, "timestamp", time())
        await self.redis_hset(key, "message", message.as_json())
        await super().put(message)

    async def get(self) -> types.Message:
        message = await super().get()
        key = self.redis_generate_key("queue", message.reply_to_message.photo[1].file_id)
        await self.redis_delete(key)
        return message


if __name__ == '__main__':
    pass
