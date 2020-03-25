import logging
from valejnik_bot.handlers import commands, messages, polls


logger = logging.getLogger("valejnik.setup_handlers")


def setup_handlers(dispatcher):
    logger.info("Setup handlers.")
    commands.register_commands(dispatcher)
    messages.register_messages(dispatcher)
    polls.register_polls(dispatcher)
