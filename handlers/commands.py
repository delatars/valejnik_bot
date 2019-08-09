# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import dispatcher, bot
from custom_filters import ChatTypeFilter
from services.auth import Auth


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['start'])
async def start(message: types.Message):
    """ `/start` """
    text = "Шалом паря! Сейчас мы начнём валежничать по полной😎\n" \
           "Скидывай мне мемасики, а уж я разберусь что с ними делать😉"
    await bot.send_message(message.chat.id, text)


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['admin'])
async def admin(message: types.Message, state: FSMContext):
    """ `/admin` """
    current_state = await state.get_state()
    if current_state == Auth.settings:
        await bot.send_message(message.chat.id, "Ты избранный, и можешь все (/settings).")
        return
    await state.set_state(Auth.check_password)
    await bot.send_message(message.chat.id, "А ну-ка дядя, напиши мне то что я хочу увидеть.")


# ################### Settings
@dispatcher.message_handler(ChatTypeFilter("private"), commands=['exit'], state=Auth.settings)
async def exit(message: types.Message, state: FSMContext):
    """ `/exit - Выйти из настроек ` """
    await state.reset_state()
    await bot.send_message(message.chat.id, "Если что ты знаешь, как вернуться😉")


@dispatcher.message_handler(ChatTypeFilter("private"), state=Auth.settings)
async def settings(message: types.Message):
    """ `/settings` """
    text = "Ты находишься в меню настроек:\n" \
           "/set_post_channel - Установить канал в который постить после модерации.\n" \
           "/set_moderate_channel - Установить канал в который отправлять на модерацию.\n" \
           "/set_timeout - Установить таймаут между постами в канал.\n" \
           "/exit - Выйти из настроек.\n"
    await bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    pass
