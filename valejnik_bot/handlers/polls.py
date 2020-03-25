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

    message_with_poll = await GroupMemePoll.get_poll(poll.id)
    if message_with_poll is None:
        return
    for option_index, option in enumerate(poll.options):
        if option["voter_count"] >= GroupMemePoll.THRESHOLD_VOTES_TO_STOP:
            await bot.stop_poll(message_with_poll.chat.id, message_with_poll.message_id)
            await GroupMemePoll.delete_poll(poll.id)
            await bot.send_message(message_with_poll.chat.id, GroupMemePoll.OPTIONS_ANSWERS[option_index],
                                   reply_to_message_id=message_with_poll.reply_to_message.message_id)
            if option_index == GroupMemePoll.INDEX_ANSWER_TO_POST:
                await MemeQueue.put(message_with_poll)
            return
    await GroupMemePoll.update_poll(poll)


async def track_private_poll(poll: types.Poll):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    UsersMemePoll = dispatcher["app"]["polls"]["users"]
    MemeQueue = dispatcher["app"]["queue"]

    message_with_poll = await UsersMemePoll.get_poll(poll.id)
    if message_with_poll is None:
        return
    for option_index, option in enumerate(poll.options):
        if option["voter_count"] >= UsersMemePoll.THRESHOLD_VOTES_TO_STOP:
            user_message = await UsersMemePoll.get_user_message(poll.id)
            await bot.stop_poll(message_with_poll.chat.id, message_with_poll.message_id)
            await UsersMemePoll.delete_poll(poll.id)
            await bot.send_message(user_message.chat.id, UsersMemePoll.OPTIONS_ANSWERS[option_index],
                                   reply_to_message_id=user_message.message_id)
            if option_index == UsersMemePoll.INDEX_ANSWER_TO_POST:
                await MemeQueue.put(message_with_poll)
            return
    await UsersMemePoll.update_poll(poll)


def register_polls(dispatcher: Dispatcher):
    dispatcher.register_poll_handler(track_private_poll, PollQuestionFilter("Ахтунг"))
    dispatcher.register_poll_handler(track_group_poll, PollQuestionFilter("Опана"))


if __name__ == '__main__':
    pass
