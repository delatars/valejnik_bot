# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.state import State, StatesGroup


class Password(StatesGroup):
    try_1 = State()
    try_2 = State()
    try_3 = State()


class Auth(StatesGroup):
    check_password = Password
    settings = State()
    banned = State()


if __name__ == '__main__':
    pass
