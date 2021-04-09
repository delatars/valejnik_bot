from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher

from valejnik_bot.custom_filters import ChatTypeFilter
from valejnik_bot.services.states import Auth
from valejnik_bot.services.ban_service import BanService


__all__ = ["register_commands"]


async def admin_banned(message: types.Message, state: FSMContext):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    banned_user = BanService.get_user(message.from_user.username)
    if banned_user.is_banned:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Ты был забанен.\n"
                                    f"Причина: {banned_user.reason}\n"
                                    f"Осталось: {banned_user.remaining_time} минут.")
    else:
        await state.reset_state()
        await admin(message, state)


async def start(message: types.Message):
    """ `/start` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    text = "Шалом паря! Сейчас мы начнём валежничать по полной😎\n" \
           "Скидывай мне мемасики, а уж я разберусь что с ними делать😉"
    await bot.send_message(chat_id=message.chat.id,
                           text=text)


async def admin(message: types.Message, state: FSMContext):
    """ `/admin` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    current_state = await state.get_state()
    if current_state == Auth.settings:
        await bot.send_message(chat_id=message.chat.id,
                               text="Ты уже избранный, и можешь все (/settings).")
        return
    await state.set_state(Auth.check_password.try_1)
    await bot.send_message(chat_id=message.chat.id,
                           text="А ну-ка дядя, напиши мне то что я хочу увидеть.")


async def exit(message: types.Message, state: FSMContext):
    """ `/exit - Выйти из настроек ` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    await state.reset_state()
    await bot.send_message(chat_id=message.chat.id,
                           text="Если что ты знаешь, как вернуться😉")


async def set_timeout(message: types.Message):
    """ `/set_timeout - Выйти из настроек ` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    config = dispatcher["config"]

    argument = message.get_args()
    if not argument:
        return await message.reply(text="Необходим аргумент <timeout: int>: Например: /set_timeout 4")
    if not argument.isdigit():
        return await message.reply(text="Аргумент <timeout> должен быть числом: Например: /set_timeout 4")
    config["bot"]["posts"]["time_between_posts"] = argument
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Установлено время между постами: {argument} мин.")


async def ban_user(message: types.Message):
    """ `/ban_user - забанить пользователя ` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot
    arguments = message.get_args()

    try:
        username, ban_time, reason = arguments.split(' ', 3)
        username, ban_time, reason = str(username), int(ban_time), str(reason)
    except ValueError:
        return await message.reply(text="Проверьте аргументы:\n -> <username: str>\n -> <time: int>\n"
                                        " -> <reason: str>\nНапример: /ban_user user 23 ушлепок")

    BanService.ban_user(username=username, ban_time=ban_time, reason=reason)
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Юзер {username}, забанен на {ban_time} мин, по причине: {reason}")


async def unban_user(message: types.Message):
    """ `/unban_user - Разбанить пользователя ` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    username = message.get_args()
    if not username:
        return await message.reply(text="Необходим аргумент <username>: Например: /unban_user user")
    if not username.isalpha():
        return await message.reply(text="Аргумент <username> должен быть строкой: Например: /unban_user user")

    BanService.unban_user(username=username)
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Юзер {username} разбанен.")


async def settings(message: types.Message):
    """ `/settings` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    text = "Ты находишься в меню настроек:\n\n" \
           "/set_timeout <timeout: int> - Установить таймаут между постами в канал.(устанавливается в минутах)\n\n" \
           "/ban_user <username: str> <time: int> <reason: str> - Забанить пользователя." \
           " (время устанавливается в минутах)\n\n" \
           "/unban_user <username: str> - Разбанить пользователя.\n\n" \
           "/exit - Выйти из настроек.\n"
    await bot.send_message(chat_id=message.chat.id,
                           text=text)


def register_commands(dispatcher):
    dispatcher.register_message_handler(start, ChatTypeFilter("private"),
                                        state="*", commands=['start'])
    dispatcher.register_message_handler(admin, ChatTypeFilter("private"),
                                        state="*", commands=['admin'])
    dispatcher.register_message_handler(admin_banned, ChatTypeFilter("private"),
                                        state=Auth.check_password.banned, commands=['admin'])

    dispatcher.register_message_handler(exit, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['exit'])
    dispatcher.register_message_handler(set_timeout, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['set_timeout'])
    dispatcher.register_message_handler(ban_user, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['ban_user'])
    dispatcher.register_message_handler(unban_user, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['unban_user'])
    dispatcher.register_message_handler(settings, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['settings'])
