# -*- coding: utf-8 -*-
import logging

from handlers import *
from misc import executor

logger = logging.getLogger("valejnik.bot")


def main():
    logger.info("Start Bot!")
    executor.start_polling()


if __name__ == '__main__':
    main()
