# -*- coding: utf-8 -*-
import asyncio
import aioredis
import logging
from misc import RedisPool

__all__ = ["RedisConnector"]


logger = logging.getLogger("valejnik.utils:RedisConnector")


def redis_db_selector(db=0):
    """ select db index execute func and return to previous index"""

    def sub_wrapper(func):

        async def wrapper(cls, *args, **kwargs):
            redis = await cls._redis()
            previous_db = redis.db
            await redis.select(db)
            logger.debug(f"Change db index to: {db}")
            result = await func(cls, *args, **kwargs)
            await redis.select(previous_db)
            logger.debug(f"Revert db index to previous: {previous_db}")
            return result

        return wrapper

    return sub_wrapper


class RedisConnector:
    REDIS_DB = 1
    REDIS_KEY_PREFIX = "polls"

    _REDIS = None
    _CONNECTION_LOCK = asyncio.Lock()

    @classmethod
    async def _redis(cls) -> aioredis.Redis:
        if cls._REDIS is None:
            cls._REDIS = await RedisPool.redis()
            logger.info(f"Created connection with: {RedisPool._host}:{RedisPool._port} db={RedisPool._db}"
                         f" with connections pool: {RedisPool._pool_size}")
        return cls._REDIS

    @classmethod
    def redis_generate_key(cls, *parts):
        return ':'.join((cls.REDIS_KEY_PREFIX, ) + tuple(map(str, parts)))

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_set(cls, key, value):
        logger.debug(f"Execute command: SET {key} {value}")
        redis = await cls._redis()
        await redis.set(key, value)

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_delete(cls, key):
        logger.debug(f"Execute command: DEL {key}")
        redis = await cls._redis()
        await redis.delete(key)

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_get(cls, key):
        logger.debug(f"Execute command: GET {key}")
        redis = await cls._redis()
        return await redis.get(key)

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_hset(cls, key, field, value):
        logger.debug(f"Execute command: HSET {key} {field} {value}")
        redis = await cls._redis()
        await redis.hset(key, field, value)

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_hget(cls, key, field):
        logger.debug(f"Execute command: HGET {key} {field}")
        redis = await cls._redis()
        return await redis.hget(key, field)

    @classmethod
    @redis_db_selector(REDIS_DB)
    async def redis_keys(cls, pattern):
        logger.debug(f"Execute command: KEYS {pattern}")
        redis = await cls._redis()
        return await redis.keys(pattern)


if __name__ == '__main__':
    pass
