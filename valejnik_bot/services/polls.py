# -*- coding: utf-8 -*-
import aioredis
import json
from aiogram import types


class GroupMemePoll:
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
    OPTIONS_ANSWERS = [
        "Mемас добавлен в очередь! Спасибо за сбор валежника.",
        "Годно, но уже баян.",
        "Мы очень пытались, но никто не заорал.",
        "Сори, но чёт сложнааааа...",
        "Слышь пёс! Отредактируй пикчу!"
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0  # INDEX OF ANSWER THAT TRIGGER POST MEME ACTION

    def __init__(self, redis_conn: aioredis.Redis):
        self.redis = redis_conn

    def redis_generate_key(self, *parts):
        return ':'.join((self.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    async def add_poll(self, message_with_poll: types.Message):
        key = self.redis_generate_key("group_meme", message_with_poll.poll.id)
        value = message_with_poll.as_json()
        await self.redis.set(key, value)

    async def delete_poll(self, poll_id: str):
        key = self.redis_generate_key("group_meme", poll_id)
        await self.redis.delete(key)

    async def get_poll(self, poll_id: str) -> types.Message or None:
        key = self.redis_generate_key("group_meme", poll_id)
        value = await self.redis.get(key)
        if value:
            return types.Message.to_object(json.loads(value))
        else:
            return None

    async def update_poll(self, poll: types.Poll) -> bool:
        key = self.redis_generate_key("group_meme", poll.id)
        value = await self.get_poll(key)
        if value is None:
            return False
        value.poll = poll
        await self.redis.set(key, value.as_json())
        return True


class UsersMemePoll:
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
    OPTIONS_ANSWERS = [
        "Годно, отправили в печать!",
        "Годно, но уже баян.",
        "Мы очень пытались, но никто не заорал.",
        "Сори, но чёт сложнааааа...",
        "Это че за колхоз?! Отредактируй пикчу!",
        "На пикче нехватает твоей мамки."
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0  # INDEX OF ANSWER THAT TRIGGER POST MEME ACTION

    def __init__(self, redis_conn: aioredis.Redis):
        self.redis = redis_conn

    def redis_generate_key(self, *parts):
        return ':'.join((self.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    async def add_poll(self, user_message: types.Message, message_with_poll: types.Message):
        key = self.redis_generate_key("user_meme", message_with_poll.poll.id)
        await self.redis.hset(key, "user_message", user_message.as_json())
        await self.redis.hset(key, "message", message_with_poll.as_json())

    async def delete_poll(self, poll_id: str):
        key = self.redis_generate_key("user_meme", poll_id)
        await self.redis.delete(key)

    async def get_poll(self, poll_id: str) -> types.Message or None:
        key = self.redis_generate_key("user_meme", poll_id)
        value = await self.redis.hget(key, "message")
        if value:
            return types.Message.to_object(json.loads(value))
        else:
            return None

    async def get_user_message(self, poll_id: str) -> types.Message or None:
        key = self.redis_generate_key("user_meme", poll_id)
        value = await self.redis.hget(key, "user_message")
        if value:
            return types.Message.to_object(json.loads(value))
        else:
            return None

    async def update_poll(self, poll: types.Poll) -> bool:
        key = self.redis_generate_key("user_meme", poll.id)
        value = await self.get_poll(key)
        if value is None:
            return False
        value.poll = poll
        await self.redis.set(key, value.as_json())
        return True
