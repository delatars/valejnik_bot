# -*- coding: utf-8 -*-
import json
from aiogram import types

from utils import RedisConnector


class GroupMemePoll(RedisConnector):
    """ Poll which will be sended after any image will be posted in group """
    QUESTION = "Опана... Новый мемасик подъехал! Аппрувим?"
    OPTIONS = [
        "Канеш.",
        "Баян.",
        "Не смешной."
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0  # INDEX OF ANSWER THAT TRIGGER POST MEME ACTION

    REDIS_DB = 1  # DB INDEX WHERE TO SAVE POLLS

    @classmethod
    async def add_poll(cls, message: types.Message):
        key = cls.redis_generate_key("group_meme", message.poll.id)
        value = message.as_json()
        await cls.redis_set(key, value)

    @classmethod
    async def delete_poll(cls, poll_id: str):
        key = cls.redis_generate_key("group_meme", poll_id)
        await cls.redis_delete(key)

    @classmethod
    async def get_poll(cls, poll_id: str) -> types.Message or None:
        key = cls.redis_generate_key("group_meme", poll_id)
        value = await cls.redis_get(key)
        if value:
            return types.Message.to_object(json.loads(value))
        else:
            return None

    @classmethod
    async def update_poll(cls, poll: types.Poll) -> bool:
        key = cls.redis_generate_key("group_meme", poll.id)
        value = await cls.get_poll(key)
        if value is None:
            return False
        value.poll = poll
        await cls.redis_set(key, value.as_json())
        return True


if __name__ == '__main__':
    pass
