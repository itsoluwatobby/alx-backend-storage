#!/usr/bin/env python3
"""
create a cache class and an instance of the redis class
"""
import redis
import uuid
import functools
from typing import Callable, Union, Optional


def count_calls(method: Callable) -> Callable:
    """
    decorator that takes a single method Callable argument
    and returns a Callable
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        increments the count for that key every time the method
        is called and returns the value returned by the original
        method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    stores the history of inputs and outputs for a particular function
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        saves the input and output of each function in redis
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))
        return output
    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a particular function"""
    val = redis.Redis()
    f_name = fn.__qualname__
    no_calls = val.get(f_name)
    try:
        no_calls = no_calls.decode('utf-8')
    except Exception:
        no_calls = 0
    print(f'{f_name} was called {no_calls} times:')

    ins = val.lrange(f_name + ":inputs", 0, -1)
    outs = val.lrange(f_name + ":outputs", 0, -1)

    for intp, outp in zip(ins, outs):
        try:
            intp = intp.decode('utf-8')
        except Exception:
            intp = ""
        try:
            outp = outp.decode('utf-8')
        except Exception:
            outp = ""

        print(f'{f_name}(*{intp}) -> {outp}')


class Cache:
    """An instance of the redis class"""
    def __init__(self):
        """Instantiates an instance of the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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

    def get(self: 'Cache', key: str, fn: Optional[callable] = None):
        """
        Takes in a key and an optional Callable
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn is not None else value

    def get_str(self: 'Cache', key: str) -> Optional[str]:
        """Gets a string value"""
        value = self._redis.get(key)
        return value.decode("UTF-8")

    def get_int(self: 'Cache', key: str) -> Optional[int]:
        """Gets an integer value"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("UTF-8"))
        except Exception as e:
            value = 0
        return value
