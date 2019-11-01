# -*- coding: utf-8 -*-
import aiohttp

# Base Settings
TELEGRAM_BOT_API_KEY = "<API KEY>"
PROXY_URL = None
PROXY_AUTH = None  # aiohttp.BasicAuth

# Redis server
REDIS_SERVER = "127.0.0.1"
REDIS_PORT = 6379

# Approved posts settings
TIME_BETWEEN_POSTS = 10  # minutes
THROTTLE_TIME_LIMIT = 5  # seconds

# Bot settings
ADMIN_PASSWORD = "qwe123"
MODERATE_CHANNEL_ID = 0
POST_CHANNEL_ID = "@test"


if __name__ == '__main__':
    pass
