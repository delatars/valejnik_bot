# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import Dispatcher

from valejnik_bot.custom_filters import PollQuestionFilter


__all__ = ["register_polls"]


async def track_group_poll(poll: types.Poll):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    GroupMemePoll = dispatcher["app"]["polls"]["group"]
    MemeQueue = dispatcher["app"]["queue"]

    poll_message = await GroupMemePoll.get_poll(poll.id)
    if poll_message is None:
        return
    for option_index, option in enumerate(poll.options):
        if option["voter_count"] >= GroupMemePoll.THRESHOLD_VOTES_TO_STOP:
            from_message = await GroupMemePoll.get_from_message(poll.id)
            await bot.stop_poll(chat_id=poll_message.chat.id,
                                message_id=poll_message.message_id)
            await GroupMemePoll.delete_poll(poll.id)
            await bot.send_message(chat_id=from_message.chat.id,
                                   text=GroupMemePoll.ANSWERS[option_index],
                                   reply_to_message_id=from_message.reply_to_message.message_id)
            if option_index == GroupMemePoll.INDEX_ANSWER_TO_POST:
                await MemeQueue.put(poll_message)
            return
    await GroupMemePoll.update_poll(poll)


async def track_private_poll(poll: types.Poll):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    UsersMemePoll = dispatcher["app"]["polls"]["users"]
    MemeQueue = dispatcher["app"]["queue"]

    poll_message = await UsersMemePoll.get_poll(poll.id)
    if poll_message is None:
        return
    for option_index, option in enumerate(poll.options):
        if option["voter_count"] >= UsersMemePoll.THRESHOLD_VOTES_TO_STOP:
            from_message = await UsersMemePoll.get_from_message(poll.id)
            await bot.stop_poll(chat_id=poll_message.chat.id,
                                message_id=poll_message.message_id)
            await UsersMemePoll.delete_poll(poll.id)
            await bot.send_message(chat_id=from_message.chat.id,
                                   text=UsersMemePoll.ANSWERS[option_index],
                                   reply_to_message_id=from_message.message_id)
            if option_index == UsersMemePoll.INDEX_ANSWER_TO_POST:
                await MemeQueue.put(poll_message)
            return
    await UsersMemePoll.update_poll(poll)


def register_polls(dispatcher: Dispatcher):
    dispatcher.register_poll_handler(track_private_poll, PollQuestionFilter("Ахтунг"))
    dispatcher.register_poll_handler(track_group_poll, PollQuestionFilter("Опана"))


if __name__ == '__main__':
    pass
