#!/usr/bin/env python3
"""
create a cache class and an instance of the redis class
"""
import redis
import uuid
import functools
from typing import Union, Optional


def count_calls(method: callable):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """An instance of the redis class"""
    def __init__(self):
        """Instantiates an instance of the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self: 'Cache', data: Union[str, bytes, int, float]) -> str:
        """
        Takes in a data argument and returns a string

        Arguments:
            data(str): a string data type
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self: 'Cache', key: str, fn: Optional[callable]=None):
        """
        Takes in a key and an optional Callable
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn is not None else value

    def get_str(self: 'Cache', key: str) -> Optional[str]:
        """Gets a string value"""
        return self._redis.get(key)

    def get_int(self: 'Cache', key: str) -> Optional[int]:
        """Gets an integer value"""
        return self._redis.get(key)
