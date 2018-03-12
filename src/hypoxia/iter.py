from typing import Iterable, Callable, Generic, TypeVar, Tuple, Optional, Iterator, Union
import functools
import itertools

_iter = iter

T = TypeVar('T')
U = TypeVar('U')


class Iter(Generic[T]):
    def __init__(self, iter: Union[Iterable[T], Iterator[T]]):
        self.iterator = _iter(iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)

    # METHODS THAT RETURN NEW ITERATORS

    def zip(self, *iters: Iterable) -> 'Iter[Tuple]':
        """Make an ``Iter`` of tuples of aligned elements from this ``Iter`` and each of the input iterables."""
        return Iter(zip(self, *iters))

    def enumerate(self, start: int = 0):
        """Return an ``Iter`` of tuples containing a count (starting from ``start``) and the elements of the original ``Iter``."""
        return Iter(enumerate(self, start = start))

    def map(self, func: Callable[[T], U]) -> 'Iter[U]':
        """Return a new ``Iter``, with each element mapped under the function ``func``."""
        return Iter(map(func, self))

    def filter(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter``, containing only elements that ``func(element)`` is true for."""
        return Iter(filter(func, self))

    # METHODS THAT COLLAPSE THE ITERATOR, RETURNING SINGLE VALUES

    def all(self) -> bool:
        """Return ``True`` if all elements of the ``Iter`` are ``True`` (or if empty)."""
        return all(self)

    def any(self) -> bool:
        """
        Return ``True`` if any element of the ``Iter`` is ``True``.
        If the ``Iter`` is empty, this returns ``False``.
        """
        return any(self)

    def reduce(self, func: Callable[[U, T], U], initial: Optional[U] = None) -> U:
        """
        Apply ``func`` cumulatively to the items in the iterable from left to right.
        The first argument of ``func`` is the accumulated value, the second is the next element of the iterable.
        If ``initial`` is given, it is first accumulated value.
        """
        return functools.reduce(func, self, initial = initial)
