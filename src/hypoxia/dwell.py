from typing import Iterable, Callable, Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Dwell(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self.iterable = iterable

    def __iter__(self):
        yield from self.iterable

    # METHODS THAT RETURN NEW ITERATORS

    def map(self, func: Callable[[T], U]) -> 'Dwell[U]':
        """Return a new ``Dwell``, with each element mapped under the function ``func``."""
        return Dwell(func(t) for t in self.iterable)

    def filter(self, func: Callable[[T], bool]) -> 'Dwell[T]':
        """Return a new ``Dwell``, containing only elements that ``func(element)`` is true for."""
        return Dwell(t for t in self.iterable if func(t))

    # METHODS THAT COLLAPSE THE ITERATOR, RETURNING SINGLE VALUES

    def all(self):
        """Return ``True`` if all elements of the ``Dwell`` are ``True`` (or if empty)."""
        return all(self)

    def any(self):
        """
        Return ``True`` if any element of the ``Dwell`` is ``True``.
        If the ``Dwell`` is empty, this returns ``False``.
        """
        return any(self)


def dwell(iterable: Iterable[T]) -> Dwell[T]:
    return Dwell(iterable)
