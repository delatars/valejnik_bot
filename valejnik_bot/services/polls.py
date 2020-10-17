# -*- coding: utf-8 -*-
import aioredis
import json
from aiogram import types
from typing import Optional


class BasePoll:

    REDIS_KEY_PREFIX = "polls"
    REDIS_KEY_POLL_NAME = ""

    QUESTION = ""
    OPTIONS = []
    ANSWERS = []
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0  # INDEX OF ANSWER THAT TRIGGER POST MEME ACTION

    def __init__(self, redis_conn: aioredis.Redis):
        self.redis = redis_conn
        if len(self.OPTIONS) != len(self.ANSWERS):
            raise TypeError(f"{self.__class__.__name__}: options and answers length should be equal")

    def redis_generate_key(self, *parts):
        return ':'.join((self.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    async def add_poll(self, poll: types.Message, from_message: types.Message):
        key = self.redis_generate_key(self.REDIS_KEY_POLL_NAME, poll.poll.id)
        await self.redis.hset(key, "poll", poll.as_json())
        await self.redis.hset(key, "from_message", from_message.as_json())

    async def delete_poll(self, poll_id: str):
        key = self.redis_generate_key(self.REDIS_KEY_POLL_NAME, poll_id)
        await self.redis.delete(key)

    async def get_poll(self, poll_id: str) -> Optional[types.Message]:
        key = self.redis_generate_key(self.REDIS_KEY_POLL_NAME, poll_id)
        value = await self.redis.hget(key, "poll")

        if value:
            return types.Message.to_object(json.loads(value))

    async def get_from_message(self, poll_id: str) -> Optional[types.Message]:
        key = self.redis_generate_key(self.REDIS_KEY_POLL_NAME, poll_id)
        value = await self.redis.hget(key, "from_message")

        if value:
            return types.Message.to_object(json.loads(value))

    async def update_poll(self, poll: types.Poll) -> bool:
        key = self.redis_generate_key(self.REDIS_KEY_POLL_NAME, poll.id)
        value = await self.get_poll(key)

        if value:
            value.poll = poll
            await self.redis.set(key, value.as_json())
            return True

        return False


class GroupMemePoll(BasePoll):
    """ Poll which will be sended after any image will be posted in group """

    REDIS_KEY_PREFIX = "polls"
    QUESTION = "Опана... Новый мемасик подъехал! Аппрувим?"
    OPTIONS = [
        "Канеш.👍",
        "Баян.🙈",
        "Не смешной.🤮",
        "Сложнаааа...🤯",
        "На редактирование!🤢👎"
    ]
    ANSWERS = [
        "Mемас добавлен в очередь! Спасибо за сбор валежника.",
        "Годно, но уже баян.",
        "Мы очень пытались, но никто не заорал.",
        "Сори, но чёт сложнааааа...",
        "Слышь пёс! Отредактируй пикчу!"
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0


class UsersMemePoll(BasePoll):
    """ Poll which will be sended after any image will be posted in group """
    REDIS_KEY_PREFIX = "polls"
    QUESTION = "Ахтунг! мемас от пользователя: "
    OPTIONS = [
        "Аппрувим.",
        "Баян.",
        "Не смешной.",
        "Сложнаааа...",
        "На редактирование!",
        "Фото члена"
    ]
    ANSWERS = [
        "Годно, отправили в печать!",
        "Годно, но уже баян.",
        "Мы очень пытались, но никто не заорал.",
        "Сори, но чёт сложнааааа...",
        "Это че за колхоз?! Отредактируй пикчу!",
        "На пикче нехватает твоей мамки."
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 1
    INDEX_ANSWER_TO_POST = 0
