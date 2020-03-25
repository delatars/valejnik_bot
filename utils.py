# -*- coding: utf-8 -*-
import logging
from misc import RedisPoolMemes


__all__ = ["RedisConnector"]


logger = logging.getLogger("valejnik.utils:RedisCoлnnector")


class RedisConnector:

    REDIS_KEY_PREFIX = "polls"

    @classmethod
    async def _redis(cls):
        return await RedisPoolMemes.redis()

    @classmethod
    def redis_generate_key(cls, *parts):
        return ':'.join((cls.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    @classmethod
    async def redis_set(cls, key, value):
        logger.debug(f"Execute command: SET {key} {value}")
        redis = await cls._redis()
        await redis.set(key, value)

    @classmethod
    async def redis_delete(cls, key):
        logger.debug(f"Execute command: DEL {key}")
        redis = await cls._redis()
        await redis.delete(key)

    @classmethod
    async def redis_get(cls, key):
        logger.debug(f"Execute command: GET {key}")
        redis = await cls._redis()
        return await redis.get(key)

    @classmethod
    async def redis_hset(cls, key, field, value):
        logger.debug(f"Execute command: HSET {key} {field} {value}")
        redis = await cls._redis()
        await redis.hset(key, field, value)

    @classmethod
    async def redis_hget(cls, key, field):
        logger.debug(f"Execute command: HGET {key} {field}")
        redis = await cls._redis()
        return await redis.hget(key, field)

    @classmethod
    async def redis_keys(cls, pattern):
        logger.debug(f"Execute command: KEYS {pattern}")
        redis = await cls._redis()
        return await redis.keys(pattern)


if __name__ == '__main__':
    pass
