from aiogram import types
from aiogram.dispatcher import Dispatcher

from valejnik_bot.custom_filters import CallbackQueryDataFilter


async def moderation_user_send(callback_query: types.CallbackQuery):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    message = callback_query.message
    UsersMemePoll = dispatcher["app"]["polls"]["users"]
    bot_config = dispatcher["config"]["bot"]["posts"]

    user_meme_message = await bot.send_photo(chat_id=bot_config["moderate_channel_id"],
                                             photo=message.reply_to_message.photo[1].file_id,
                                             disable_notification=UsersMemePoll.DISABLE_NOTIFICATION)
    question = f"{UsersMemePoll.QUESTION}: @{message.from_user.username}\n" \
               f"Доп. инфа:\n" \
               f"Bot: {'Да' if message.from_user.is_bot else 'Нет'} | " \
               f"UserName: {message.from_user.username} | " \
               f"- LastName: {message.from_user.last_name} | " \
               f"- FirstName: {message.from_user.first_name}"
    poll = await bot.send_poll(chat_id=bot_config["moderate_channel_id"],
                               question=question,
                               options=UsersMemePoll.OPTIONS,
                               disable_notification=UsersMemePoll.DISABLE_NOTIFICATION,
                               reply_to_message_id=user_meme_message.message_id)
    await UsersMemePoll.add_poll(poll, message)
    await bot.send_message(chat_id=message.chat.id,
                           text="Мемас отправлен на модерацию. Благодарим вас за помощь в сборе валежника.")

    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=callback_query.message.message_id)


async def moderation_group_send(callback_query: types.CallbackQuery):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    message = callback_query.message
    GroupMemePoll = dispatcher["app"]["polls"]["group"]

    poll = await bot.send_poll(chat_id=message.chat.id,
                               question=GroupMemePoll.QUESTION,
                               options=GroupMemePoll.OPTIONS,
                               disable_notification=GroupMemePoll.DISABLE_NOTIFICATION,
                               reply_to_message_id=message.reply_to_message.message_id)
    await GroupMemePoll.add_poll(poll, message)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)


async def moderation_dismiss(callback_query: types.CallbackQuery):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)


def register_queries(dispatcher):
    dispatcher.register_callback_query_handler(moderation_user_send,
                                               CallbackQueryDataFilter('moderation_user_send'), state="*")
    dispatcher.register_callback_query_handler(moderation_group_send,
                                               CallbackQueryDataFilter('moderation_group_send'), state="*")
    dispatcher.register_callback_query_handler(moderation_dismiss,
                                               CallbackQueryDataFilter('moderation_dismiss'), state="*")


if __name__ == '__main__':
    pass
