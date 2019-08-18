# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import dispatcher, bot
from custom_filters import ChatTypeFilter
from services.auth import Auth, Banned
import config


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['admin'], state=Auth.check_password.banned)
async def any_message(message: types.Message, state: FSMContext):
    remaining = Banned.is_ban(message.from_user.username)
    if remaining:
        await bot.send_message(message.chat.id, f"Ты был забанен на 1 час. Осталось: {remaining} минут.")
    else:
        await state.reset_state()
        await admin(message, state)


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
        await bot.send_message(message.chat.id, "Ты уже избранный, и можешь все (/settings).")
        return
    await state.set_state(Auth.check_password.try_1)
    await bot.send_message(message.chat.id, "А ну-ка дядя, напиши мне то что я хочу увидеть.")


# ################### Settings
@dispatcher.message_handler(ChatTypeFilter("private"), commands=['exit'], state=Auth.settings)
async def exit(message: types.Message, state: FSMContext):
    """ `/exit - Выйти из настроек ` """
    await state.reset_state()
    await bot.send_message(message.chat.id, "Если что ты знаешь, как вернуться😉")


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['set_timeout'], state=Auth.settings)
async def set_timeout(message: types.Message):
    """ `/set_timeout - Выйти из настроек ` """
    argument = message.get_args()
    if not argument:
        return await message.reply("Необходим аргумент <timeout>: Например: /set_timeout 4")
    if not argument.isdigit():
        return await message.reply("Аргумент <timeout> должен быть числом: Например: /set_timeout 4")
    config.TIME_BETWEEN_POSTS = argument
    await bot.send_message(message.chat.id, f"Установлено время между постами: {argument} мин.")


@dispatcher.message_handler(ChatTypeFilter("private"), state=Auth.settings)
async def settings(message: types.Message):
    """ `/settings` """
    text = "Ты находишься в меню настроек:\n\n" \
           "/set_post_channel <channel_id> - Установить канал в который постить после модерации.\n\n" \
           "/set_moderate_channel <channel_id> - Установить канал в который отправлять на модерацию.\n\n" \
           "/set_timeout <timeout> - Установить таймаут между постами в канал.(устанавливается в минутах)\n\n" \
           "/exit - Выйти из настроек.\n"
    await bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    pass
