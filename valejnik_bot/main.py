import argparse
import logging
import os
import re
import ssl
import sys
import yaml

from aiohttp import BasicAuth
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import *
from aiogram.utils.executor import start_polling, start_webhook
from subprocess import Popen, PIPE
from yarl import URL

from valejnik_bot.pre_post_processing import on_startup, on_shutdown


logger = logging.getLogger("valejnik.main")


def configure_logging(mode):
    logging.basicConfig(
        level=logging.DEBUG if mode else logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )


def parse_args():
    parser = argparse.ArgumentParser(description='Python telegram bot')
    parser.add_argument('--mode', '-m', choices=['polling', 'webhook'],
                        help='Set bot mode: polling|webhook')
    parser.add_argument('--edit', '-e', action='store_true', default=False, help='Edit config file.')
    parser.add_argument('--show', '-s', action='store_true', default=False, help='Show config file.')
    parser.add_argument('--config', '-c', type=str, default=False, help='Specify config file to use.')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Enable debug mode')

    argv = sys.argv[1:]
    if not len(argv):
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(argv)


def load_config(config_path):
    logger.info(f"Load configuration file: {config_path}")
    with open(config_path, "r") as cfg_file:
        cfg = yaml.safe_load(cfg_file.read())
    return cfg


def show_config(filepath):
    Popen(f"cat {filepath}", shell=True, stderr=PIPE).communicate()


def edit_config(filepath):

    editor = None
    default_editor = "/usr/bin/vi"
    selected_editor_path = os.path.join(os.path.expanduser("~"), ".selected_editor")

    def get_editor():
        with open(selected_editor_path, "r") as se_file:
            finded = re.findall(r'SELECTED_EDITOR="([^\n]+)"', se_file.read())
            if finded:
                return finded[0]

    if os.path.exists(selected_editor_path):
        editor = get_editor()
    else:
        _, stderr = Popen("select-editor", shell=True, stderr=PIPE).communicate()
        if len(stderr) == 0:
            editor = get_editor()

    Popen([editor or default_editor, filepath]).communicate()


def start_bot(mode, config):

    api = config["general"]["api"]

    token = api["token"]
    webhook_url = URL(api["webhook"]["url"]) if api["webhook"]["url"] else None
    cert = api["webhook"]["cert"]
    pkey = api["webhook"]["pkey"]
    proxy_url = api["proxy"]["url"]

    if not api["proxy"]["login"] or not api["proxy"]["password"]:
        proxy_auth = None
    else:
        proxy_auth = BasicAuth(login=api["proxy"]["login"], password=api["proxy"]["password"])

    # Create bot & dispatcher instances.
    bot = Bot(token, proxy=proxy_url, proxy_auth=proxy_auth)
    dispatcher = Dispatcher(bot)
    dispatcher["config"] = config
    logger.info(f"Initialize dispatcher: {dispatcher}")

    if mode == "webhook":
        if cert and pkey:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(cert, pkey)
        else:
            ssl_context = None

        start_webhook(dispatcher, webhook_url.path,
                      on_startup=on_startup, url=str(webhook_url), cert=cert,
                      on_shutdown=on_shutdown,
                      host=webhook_url.host, port=webhook_url.port, ssl_context=ssl_context)
    else:
        start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)


def main():
    args = parse_args()

    if args.config:
        config_path = args.config
    else:
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

    if args.show:
        show_config(config_path)
        sys.exit(0)

    if args.edit:
        edit_config(config_path)
        sys.exit(0)

    configure_logging(args.debug)
    start_bot(args.mode, load_config(config_path))


if __name__ == '__main__':
    main()
