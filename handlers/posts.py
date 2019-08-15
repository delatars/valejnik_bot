# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.types.message import ContentType

from tasks import MemeQueue
from misc import dispatcher, bot
from services.polls import GroupMemePoll
from custom_filters import ChatTypeFilter


@dispatcher.poll_handler()
async def track_poll(poll: types.Poll):
    message = await GroupMemePoll.get_poll(poll.id)
    if message is None:
        return
    for option_index, option in enumerate(poll.options):
        if option["voter_count"] >= GroupMemePoll.THRESHOLD_VOTES_TO_STOP:
            await bot.stop_poll(message.chat.id, message.message_id)
            await GroupMemePoll.delete_poll(poll.id)
            if option_index == GroupMemePoll.INDEX_ANSWER_TO_POST:
                await MemeQueue.put(message)
                await bot.send_message(message.chat.id, "Mемас добавлен в очередь! Спасибо за сбор валежника.",
                                       reply_to_message_id=message.reply_to_message.message_id)
                return
            else:
                await bot.send_message(message.chat.id, "Сорян, но походу мемас оказался не очень.",
                                       reply_to_message_id=message.reply_to_message.message_id)
                return
    await GroupMemePoll.update_poll(poll)


@dispatcher.message_handler(ChatTypeFilter("group"), content_types=ContentType.PHOTO)
async def group_meme(message: types.Message):
    message = await bot.send_poll(message.chat.id, GroupMemePoll.QUESTION, GroupMemePoll.OPTIONS,
                                  GroupMemePoll.DISABLE_NOTIFICATION, message.message_id)
    await GroupMemePoll.add_poll(message)


@dispatcher.message_handler(ChatTypeFilter("private"), content_types=ContentType.PHOTO)
async def private_meme(message: types.Message):
    # Todo пересылать мемасы на модерацию
    await bot.send_message(message.chat.id, "Мемас отправлен на модерацию. Благодарим вас за помощь в сборе валежника.")


if __name__ == '__main__':
    pass
