# -*- coding: utf-8 -*-
from aiogram import types

from misc import dispatcher, bot


@dispatcher.message_handler()
async def text_message(message: types.Message):
    if message.chat.type != "group":
        await bot.send_message(message.chat.id, "Моя вас не понимать, я уважаю только мемасы.")


if __name__ == '__main__':
    pass
