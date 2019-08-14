# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType

from misc import dispatcher, bot
from custom_filters import ChatTypeFilter
from services.auth import Auth, Banned
from config import ADMIN_PASSWORD


@dispatcher.message_handler(
    ChatTypeFilter("private"), state=[Auth.check_password.try_1, Auth.check_password.try_2,
                                      Auth.check_password.try_3, Auth.check_password.last],
    content_types=ContentType.TEXT
)
async def check_password(message: types.Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await state.set_state(Auth.settings)
        await bot.send_message(message.chat.id, "О боги, ты избранный!\nНааа... валяй, что вздумается /settings")
    else:
        current_state = await state.get_state()
        if current_state == Auth.check_password.try_1.state:
            await bot.send_message(message.chat.id, "Херня какая-то, наверное ты что-то не то ввел\n"
                                                    "Давай-ка еще разок попробуй.")
            await state.set_state(Auth.check_password.try_2)
        elif current_state == Auth.check_password.try_2.state:
            await bot.send_message(message.chat.id, "Ну ты криворукий канеш)\n"
                                                    "Давай-ка еще разок попробуй.")
            await state.set_state(Auth.check_password.try_3)
        elif current_state == Auth.check_password.try_3.state:
            await bot.send_message(message.chat.id, "Ты чё это взломать меня удумал?\n"
                                                    "Ладно дам тебе еще шанс.")
            await state.set_state(Auth.check_password.last)
        elif current_state == Auth.check_password.last.state:
            await bot.send_message(message.chat.id, "Ну все дядя, ты доигрался, увидимся через час.")
            Banned.add_user(message.from_user.username)
            await state.set_state(Auth.check_password.banned)


@dispatcher.message_handler(ChatTypeFilter("private"), state=[Auth.check_password.try_1, Auth.check_password.try_2,
                                                              Auth.check_password.try_3, Auth.check_password.last])
async def failed_password_type(message: types.Message):
    """ If password type is invalid """
    return await message.reply("Дядя ты нормальный?! Даже ребенок знает что пароль это набор символов.\n"
                               "Давай-ка еще разок попробуй.")


@dispatcher.message_handler(ChatTypeFilter("private"), state="*")
async def any_message(message: types.Message):
    await bot.send_message(message.chat.id, "Моя вас не понимать, я уважаю только мемасы.")


if __name__ == '__main__':
    pass
