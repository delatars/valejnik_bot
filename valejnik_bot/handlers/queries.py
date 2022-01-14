from aiogram import types
from aiogram.dispatcher import Dispatcher

from valejnik_bot.custom_filters import CallbackQueryDataFilter


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
    dispatcher.register_callback_query_handler(moderation_group_send,
                                               CallbackQueryDataFilter('moderation_group_send'), state="*")
    dispatcher.register_callback_query_handler(moderation_dismiss,
                                               CallbackQueryDataFilter('moderation_dismiss'), state="*")
