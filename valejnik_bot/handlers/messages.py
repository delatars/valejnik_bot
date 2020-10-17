# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.types.message import ContentType

from valejnik_bot.custom_filters import ChatTypeFilter, ChatIdFilter
from valejnik_bot.services.auth import Auth, Banned


__all__ = ["register_messages"]


async def throttled_message(*args, **kwargs):
    dispatcher = Dispatcher.get_current()
    config = dispatcher["config"]
    throttle_time_limit = config["bot"]["posts"]["throttle_time_limit"]
    message = args[0]
    val = f'{throttle_time_limit} секунд.' if throttle_time_limit // 60 == 0 else \
        f'{throttle_time_limit // 60} минут.'
    await message.answer(text=f"Извините, но мемасы можно отправлять раз в {val}\nПожалуйста подождите...")


async def check_password(message: types.Message, state: FSMContext):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    config = dispatcher["config"]

    if message.text == config["bot"]["admin"]["password"]:
        await state.set_state(Auth.settings)
        await bot.send_message(chat_id=message.chat.id,
                               text="О боги, ты избранный!\nНааа... валяй, что вздумается /settings")
    else:
        current_state = await state.get_state()
        if current_state == Auth.check_password.try_1.state:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Херня какая-то, наверное ты что-то не то ввел\n"
                                        "Давай-ка еще разок попробуй.")
            await state.set_state(Auth.check_password.try_2)
        elif current_state == Auth.check_password.try_2.state:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Ну ты криворукий канеш)\nДавай-ка еще разок попробуй.")
            await state.set_state(Auth.check_password.try_3)
        elif current_state == Auth.check_password.try_3.state:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Ты чё это взломать меня удумал?\nЛадно дам тебе еще шанс.")
            await state.set_state(Auth.check_password.last)
        elif current_state == Auth.check_password.last.state:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Ну все дядя, ты доигрался, увидимся через час.")
            Banned.add_user(message.from_user.username)
            await state.set_state(Auth.check_password.banned)


async def failed_password_type(message: types.Message):
    """ If password type is invalid """
    return await message.reply(text="Дядя ты нормальный?! Даже ребенок знает что пароль это набор символов.\n"
                               "Давай-ка еще разок попробуй.")


async def any_message(message: types.Message):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    await bot.send_message(chat_id=message.chat.id,
                           text="Моя вас не понимать, я уважаю только мемасы.")


async def create_group_poll(message: types.Message):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    GroupMemePoll = dispatcher["app"]["polls"]["group"]

    poll = await bot.send_poll(chat_id=message.chat.id,
                               question=GroupMemePoll.QUESTION,
                               options=GroupMemePoll.OPTIONS,
                               disable_notification=GroupMemePoll.DISABLE_NOTIFICATION,
                               reply_to_message_id=message.message_id)
    await GroupMemePoll.add_poll(poll, message)


async def create_private_poll(message: types.Message):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    bot_config = dispatcher["config"]["bot"]["posts"]
    UsersMemePoll = dispatcher["app"]["polls"]["users"]

    user_meme_message = await bot.send_photo(chat_id=bot_config["moderate_channel_id"],
                                             photo=message.photo[1].file_id,
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


def register_messages(dispatcher):
    bot_config = dispatcher["config"]["bot"]["posts"]

    # Auth handlers
    dispatcher.register_message_handler(
        check_password, ChatTypeFilter("private"),
        state=[Auth.check_password.try_1, Auth.check_password.try_2,
               Auth.check_password.try_3, Auth.check_password.last],
        content_types=ContentType.TEXT
    )
    dispatcher.register_message_handler(
        failed_password_type,
        ChatTypeFilter("private"),
        state=[Auth.check_password.try_1, Auth.check_password.try_2,
               Auth.check_password.try_3, Auth.check_password.last]
    )

    # Polls messages
    dispatcher.register_message_handler(create_group_poll, ChatTypeFilter("group"),
                                        ChatIdFilter(bot_config["moderate_channel_id"]),
                                        content_types=ContentType.PHOTO)
    private_poll_callback = dispatcher.throttled(throttled_message, rate=bot_config["throttle_time_limit"])(create_private_poll)
    dispatcher.register_message_handler(private_poll_callback, ChatTypeFilter(["private", "group"]),
                                        content_types=ContentType.PHOTO)

    # Any message
    dispatcher.register_message_handler(any_message, ChatTypeFilter("private"), state="*")


if __name__ == '__main__':
    pass
