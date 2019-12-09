# -*- coding: utf-8 -*-
import config
from aiogram import types
from aiogram.types.message import ContentType

from tasks import MemeQueue
from misc import dispatcher, bot
from services.polls import GroupMemePoll, UsersMemePoll
from custom_filters import ChatTypeFilter, ChatIdFilter, PollQuestionFilter


async def throttled_message(*args, **kwargs):
    message = args[0]
    val = f"{config.THROTTLE_TIME_LIMIT} секунд." if config.THROTTLE_TIME_LIMIT // 60 == 0 else \
        f"{config.THROTTLE_TIME_LIMIT // 60} минут."
    await message.answer(f"Извините, но мемасы можно отправлять раз в {val}\nПожалуйста подождите...")


@dispatcher.poll_handler(PollQuestionFilter("Опана"))
async def track_group_poll(poll: types.Poll):
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


@dispatcher.poll_handler(PollQuestionFilter("Ахтунг"))
async def track_users_poll(poll: types.Poll):
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


@dispatcher.message_handler(ChatTypeFilter("group"), ChatIdFilter(config.MODERATE_CHANNEL_ID),
                            content_types=ContentType.PHOTO)
async def group_meme(message: types.Message):
    message = await bot.send_poll(message.chat.id, GroupMemePoll.QUESTION, GroupMemePoll.OPTIONS,
                                  GroupMemePoll.DISABLE_NOTIFICATION, message.message_id)
    await GroupMemePoll.add_poll(message)


@dispatcher.message_handler(ChatTypeFilter(["private", "group"]), content_types=ContentType.PHOTO)
@dispatcher.throttled(throttled_message, rate=config.THROTTLE_TIME_LIMIT)
async def private_meme(message: types.Message):
    user_meme_message = await bot.send_photo(config.MODERATE_CHANNEL_ID, message.photo[1].file_id,
                                             disable_notification=UsersMemePoll.DISABLE_NOTIFICATION)
    question = f"{UsersMemePoll.QUESTION}: @{message.from_user.username}\n" \
               f"Доп. инфа:\n" \
               f"Bot: {'Да' if message.from_user.is_bot else 'Нет'} | " \
                f"UserName: {message.from_user.username} | " \
                f"- LastName: {message.from_user.last_name} | " \
                f"- FirstName: {message.from_user.first_name}"
    message_with_poll = await bot.send_poll(config.MODERATE_CHANNEL_ID, question, UsersMemePoll.OPTIONS,
                                            UsersMemePoll.DISABLE_NOTIFICATION, user_meme_message.message_id)
    await UsersMemePoll.add_poll(message, message_with_poll)
    await bot.send_message(message.chat.id, "Мемас отправлен на модерацию. Благодарим вас за помощь в сборе валежника.")


if __name__ == '__main__':
    pass
