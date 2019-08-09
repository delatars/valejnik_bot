# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType

from misc import dispatcher, bot
from custom_filters import ChatTypeFilter
from services.auth import Auth
from config import ADMIN_PASSWORD


@dispatcher.message_handler(lambda message: not message.content_type == ContentType.TEXT, state=Auth.check_password)
async def failed_password_type(message: types.Message):
    """ If password type is invalid """
    return await message.reply("Дядя ты нормальный?! Даже ребенок знает что пароль это набор символов.\n"
                               "Давай-ка еще разок попробуй.")


@dispatcher.message_handler(
    ChatTypeFilter("private"), state=Auth.check_password
)
async def check_password(message: types.Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await state.set_state(Auth.settings)
        await bot.send_message(message.chat.id, "О боги, ты избранный!\nНааа... валяй, что вздумается /settings")
    else:
        await bot.send_message(message.chat.id, "Херня какая-то, наверное ты что-то не то ввел\n"
                                                "Давай-ка еще разок попробуй.")
        # current_state = await state.get_state()
        # await Auth.check_password.next()


@dispatcher.message_handler(ChatTypeFilter("private"))
async def any_message(message: types.Message):
    await bot.send_message(message.chat.id, "Моя вас не понимать, я уважаю только мемасы.")


if __name__ == '__main__':
    pass
