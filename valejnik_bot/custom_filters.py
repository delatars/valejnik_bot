from aiogram.dispatcher.filters.filters import BoundFilter
from aiogram import types

from typing import Union, List, Tuple


class ChatTypeFilter(BoundFilter):
    """
    chat_types:
        - private
        - group
        - super_group
        - channel
    """
    key = 'chat_type'

    def __init__(self, chat_type: Union[str, List, Tuple]):
        self.chat_type = chat_type

    async def check(self, message: types.Message) -> bool:
        if isinstance(self.chat_type, (tuple, list)):
            return message.chat.type in self.chat_type
        else:
            return message.chat.type == self.chat_type


class ChatIdFilter(BoundFilter):

    key = 'chat_id'

    def __init__(self, chat_id: str):
        self.chat_id = str(chat_id)

    async def check(self, message: types.Message) -> bool:
        return str(message.chat.id) == self.chat_id


class PollQuestionFilter(BoundFilter):
    key = 'question'

    def __init__(self, question: str):
        if isinstance(question, str):
            self.question = question
        else:
            self.question = ""

    async def check(self, poll: types.Poll) -> bool:
        return self.question in poll.question


class CallbackQueryDataFilter(BoundFilter):

    key = 'data'

    def __init__(self, data: str):
        self.data = str(data)

    async def check(self, query: types.CallbackQuery) -> bool:
        return str(query.data) == self.data


if __name__ == '__main__':
    pass
