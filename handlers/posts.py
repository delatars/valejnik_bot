# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.types.message import ContentType

from misc import dispatcher, bot, MemeQueue
from services.polls import MemePoll
from custom_filters import ChatTypeFilter


@dispatcher.poll_handler()
async def track_poll(poll: types.Poll):
    for poll_index, message in enumerate(MemePoll.ACTIVE_POLLS):
        if poll.id == message.poll.id:
            for option_index, option in enumerate(poll.options):
                if option["voter_count"] >= MemePoll.THRESHOLD_VOTES_TO_STOP:
                    await bot.stop_poll(message.chat.id, message.message_id)
                    MemePoll.ACTIVE_POLLS.pop(poll_index)
                    if option_index == MemePoll.INDEX_ANSWER_TO_POST:
                        await MemeQueue.put(message.reply_to_message.photo[1])
                        await bot.send_message(message.chat.id, "Mемас добавлен в очередь! Спасибо за сбор валежника.",
                                               reply_to_message_id=message.reply_to_message.message_id)
                    else:
                        await bot.send_message(message.chat.id, "Сорян, но походу мемас оказался не очень.",
                                               reply_to_message_id=message.reply_to_message.message_id)


@dispatcher.message_handler(ChatTypeFilter("group"), content_types=ContentType.PHOTO)
async def group_meme(message: types.Message):
    message = await bot.send_poll(message.chat.id, MemePoll.QUESTION, MemePoll.OPTIONS,
                                  MemePoll.DISABLE_NOTIFICATION, message.message_id)
    MemePoll.ACTIVE_POLLS.append(message)


@dispatcher.message_handler(ChatTypeFilter("private"), content_types=ContentType.PHOTO)
async def private_meme(message: types.Message):
    # Todo пересылать мемасы на модерацию
    await bot.send_message(message.chat.id, "Мемас отправлен на модерацию. Благодарим вас за помощь в сборе валежника.")


if __name__ == '__main__':
    pass
