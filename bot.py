# -*- coding: utf-8 -*-
import logging

from misc import executor
from tasks import loop
from handlers import *

logger = logging.getLogger("valejnik.bot")


def main():
    # init tasks
    executor.loop = loop

    logger.info("Start Bot!")
    executor.start_polling()


if __name__ == '__main__':
    main()
