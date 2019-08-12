# -*- coding: utf-8 -*-


class MemePoll:
    """ Poll which will be sended after any image will be posted in group """
    QUESTION = "Опана... Новый мемасик подъехал! Аппрувим?"
    OPTIONS = [
        "Канеш.",
        "Баян.",
        "Не смешной."
    ]
    DISABLE_NOTIFICATION = True
    THRESHOLD_VOTES_TO_STOP = 2
    INDEX_ANSWER_TO_POST = 0  # OPTIONS[0]
    ACTIVE_POLLS = []  # Currently active polls (not closed)


if __name__ == '__main__':
    pass
