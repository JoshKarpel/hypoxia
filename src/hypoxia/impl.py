from typing import Type


def impl(cls: Type):
    """A decorator that adds a method to a class."""

    def wrapper(func):
        setattr(cls, func.__name__, func)

    return wrapper
