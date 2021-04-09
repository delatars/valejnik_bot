# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import time


class Password(StatesGroup):
    try_1 = State()
    try_2 = State()
    try_3 = State()
    try_last = State()
    banned = State()


class Auth(StatesGroup):
    check_password = Password
    settings = State()
    banned = State()
