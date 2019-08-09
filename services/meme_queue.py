# -*- coding: utf-8 -*-
import asyncio
from aiogram.utils.exceptions import NeedAdministratorRightsInTheChannel
from aiogram import Bot

__all__ = ["AsyncQueue"]


class AsyncQueue(asyncio.Queue):

    SEND_POSTS_TO = "@Valejnick"
    DISABLE_NOTIFICATION = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start_posting(self, control: Bot, timeout=1):
        """ Get meme from queue and post it.

        :type timeout: int: time (in minutes) to sleep between next post
        """
        while 1:
            meme = await self.get()
            try:
                await control.send_photo(self.SEND_POSTS_TO, meme.file_id,
                                         disable_notification=self.DISABLE_NOTIFICATION)
            except NeedAdministratorRightsInTheChannel:
                await control.send_message(meme.chat.id, f"Мне нужны права администратора на отправку сообщений,"
                                                         f" чтобы отправить пост в канал: {self.SEND_POSTS_TO}")
            else:
                await asyncio.sleep(timeout*60)


if __name__ == '__main__':
    pass
