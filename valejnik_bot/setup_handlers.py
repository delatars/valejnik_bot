import logging
from valejnik_bot.handlers import commands, messages, polls, queries


logger = logging.getLogger("valejnik.setup_handlers")


def setup_handlers(dispatcher):
    logger.info("Setup handlers.")
    queries.register_queries(dispatcher)
    commands.register_commands(dispatcher)
    messages.register_messages(dispatcher)
    polls.register_polls(dispatcher)
