# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import time


class Password(StatesGroup):
    try_1 = State()
    try_2 = State()
    try_3 = State()
    last = State()
    banned = State()


class Auth(StatesGroup):
    check_password = Password
    settings = State()
    banned = State()


class Banned:
    BAN_TIME = 60 * 60  # 1 hour
    USERS = {}

    @classmethod
    def add_user(cls, username):
        cls.USERS[str(username)] = time()

    @classmethod
    def is_ban(cls, username):
        if username in cls.USERS:
            elapsed = time() - cls.USERS[str(username)]
            if elapsed < cls.BAN_TIME:
                remaining = cls.BAN_TIME - elapsed
                return round(remaining) // 60
        return 0


if __name__ == '__main__':
    pass
