from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher

from valejnik_bot.custom_filters import ChatTypeFilter
from valejnik_bot.services.auth import Auth, Banned


__all__ = ["register_commands"]


async def admin_banned(message: types.Message, state: FSMContext):
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    remaining = Banned.is_ban(message.from_user.username)
    if remaining:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Ты был забанен на 1 час. Осталось: {remaining} минут.")
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
        return await message.reply(text="Необходим аргумент <timeout>: Например: /set_timeout 4")
    if not argument.isdigit():
        return await message.reply(text="Аргумент <timeout> должен быть числом: Например: /set_timeout 4")
    config["bot"]["posts"]["time_between_posts"] = argument
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Установлено время между постами: {argument} мин.")


async def settings(message: types.Message):
    """ `/settings` """
    dispatcher = Dispatcher.get_current()
    bot = dispatcher.bot

    text = "Ты находишься в меню настроек:\n\n" \
           "/set_post_channel <channel_id> - Установить канал в который постить после модерации.\n\n" \
           "/set_moderate_channel <channel_id> - Установить канал в который отправлять на модерацию.\n\n" \
           "/set_timeout <timeout> - Установить таймаут между постами в канал.(устанавливается в минутах)\n\n" \
           "/exit - Выйти из настроек.\n"
    await bot.send_message(chat_id=message.chat.id,
                           text=text)


def register_commands(dispatcher):
    dispatcher.register_message_handler(start, ChatTypeFilter("private"), commands=['start'], state="*")
    dispatcher.register_message_handler(admin, ChatTypeFilter("private"), commands=['admin'], state="*")
    dispatcher.register_message_handler(admin_banned, ChatTypeFilter("private"),
                                        state=Auth.check_password.banned, commands=['admin'])
    dispatcher.register_message_handler(exit, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['exit'])
    dispatcher.register_message_handler(set_timeout, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['set_timeout'])
    dispatcher.register_message_handler(settings, ChatTypeFilter("private"),
                                        state=Auth.settings, commands=['settings'])


if __name__ == '__main__':
    pass
