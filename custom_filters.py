# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.filters import BoundFilter
from aiogram import types


class ChatTypeFilter(BoundFilter):
    """
    chat_types:
        - private
        - group
        - super_group
        - channel
    """
    key = 'chat_type'

    def __init__(self, chat_type: str):
        if isinstance(chat_type, str):
            self.chat_type = chat_type
        else:
            self.chat_type = ""

    async def check(self, message: types.Message) -> bool:
        return message.chat.type == self.chat_type


if __name__ == '__main__':
    pass
