from typing import Type


def impl(*cls: Type):
    """A decorator that adds a method to classes."""

    def wrapper(func):
        for c in cls:
            setattr(c, func.__name__, func)

    return wrapper
