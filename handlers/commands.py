# -*- coding: utf-8 -*-
from aiogram import types

from misc import dispatcher, bot
from custom_filters import ChatTypeFilter


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['start'])
async def start(message: types.Message):
    """ `/start` """
    text = "Шалом паря! Сейчас мы начнём валежничать по полной😎\n" \
           "Но для начала ты должен доказать что ты достоин!\n" \
           "Нажми сюда, чтобы проверить это: /admin"
    await bot.send_message(message.chat.id, text)


@dispatcher.message_handler(ChatTypeFilter("private"), commands=['admin'])
async def admin(message: types.Message):
    """ `/admin` """
    text = "А ну-ка дядя, напиши мне то что я хочу увидеть."
    await bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    pass
