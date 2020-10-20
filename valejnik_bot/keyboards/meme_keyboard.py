from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


__all__ = [
    "meme_user_action_keyboard",
    "meme_group_action_keyboard"
]


moderation_user_send_button = InlineKeyboardButton('Отправить на модерацию', callback_data='moderation_user_send')
moderation_group_send_button = InlineKeyboardButton('На модерацию', callback_data='moderation_group_send')
moderation_dissmiss_button = InlineKeyboardButton('Нет', callback_data='moderation_dismiss')

meme_user_action_keyboard = InlineKeyboardMarkup()
meme_user_action_keyboard.add(moderation_user_send_button)
meme_user_action_keyboard.add(moderation_dissmiss_button)

meme_group_action_keyboard = InlineKeyboardMarkup()
meme_group_action_keyboard.add(moderation_group_send_button)
meme_group_action_keyboard.add(moderation_dissmiss_button)
