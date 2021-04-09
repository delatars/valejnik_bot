# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.types.message import ContentType

from valejnik_bot.custom_filters import ChatTypeFilter, ChatIdFilter
from valejnik_bot.services.states import Auth
from valejnik_bot.services.ban_service import BanService
from valejnik_bot.keyboards.meme_keyboard import meme_user_action_keyboard, meme_group_action_keyboard


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

    async def process_message(response_text, user_state):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.set_state(user_state)
        await bot.send_message(chat_id=message.chat.id, text=response_text)

    if message.text == config["bot"]["admin"]["password"]:
        await process_message(
            "О боги, ты избранный!\nНааа... валяй, что вздумается /settings",
            Auth.settings,
        )
    else:
        current_state = await state.get_state()
        if current_state == Auth.check_password.try_1.state:
            await process_message(
                "Херня какая-то, наверное ты что-то не то ввел\nДавай-ка еще разок попробуй.",
                Auth.check_password.try_2,
            )
        elif current_state == Auth.check_password.try_2.state:
            await process_message(
                "Ну ты криворукий канеш)\nДавай-ка еще разок попробуй.",
                Auth.check_password.try_3,
            )
        elif current_state == Auth.check_password.try_3.state:
            await process_message(
                "Ты чё это взломать меня удумал?\nЛадно дам тебе еще шанс.",
                Auth.check_password.try_last,
            )
        elif current_state == Auth.check_password.try_last.state:
            BanService.ban_user(message.from_user.username, 'Перебирал пароль.')
            await process_message(
                "Ну все дядя, ты доигрался, увидимся через час.",
                Auth.check_password.banned,
            )


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
    await message.reply("Пахнет мемасом, че с ним делаем?", reply_markup=meme_group_action_keyboard)


async def create_private_poll(message: types.Message):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    if BanService.user_is_banned(message.from_user.username):
        banned_user = BanService.get_user(message.from_user.username)
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Вы были забанены и не можете отправлять мемасы в канал.\n"
                                    f"Причина: {banned_user.reason}\n"
                                    f"Осталось: {banned_user.remaining_time} минут.")
        return

    await message.reply("Опа мемасик, че с ним делаем?", reply_markup=meme_user_action_keyboard)


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
    dispatcher.register_message_handler(create_group_poll,
                                        ChatTypeFilter("group"),
                                        ChatIdFilter(bot_config["moderate_channel_id"]),
                                        content_types=ContentType.PHOTO,
                                        state="*")
    private_poll_callback = dispatcher.throttled(throttled_message,
                                                 rate=bot_config["throttle_time_limit"])(create_private_poll)
    dispatcher.register_message_handler(private_poll_callback,
                                        ChatTypeFilter(["private", "group"]),
                                        content_types=ContentType.PHOTO,
                                        state="*")

    # Any message
    dispatcher.register_message_handler(any_message, ChatTypeFilter("private"), state="*")
