from typing import Iterable, Callable, Generic, TypeVar, Tuple, Optional, Iterator, Union, List, Any
import functools
import itertools

from .option import Option, Some, Nun

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

    def chain(self, *iters) -> 'Iter':
        return Iter(itertools.chain(*iters))

    def zip(self, *iters: Iterable) -> 'Iter[Tuple]':
        """Make an ``Iter`` of tuples of aligned elements from this ``Iter`` and each of the input iterables."""
        return Iter(zip(self, *iters))

    def zip_longest(self, *iters: Iterable, fill = None) -> 'Iter[Tuple]':
        return Iter(itertools.zip_longest(self, *iters, fillvalue = fill))

    def unzip(self) -> List[List]:
        """Unzip an ``Iter`` into lists."""
        first = next(self)
        out = [[element] for element in first]

        for t in self:
            for out_list, element in zip(out, t):
                out_list.append(element)

        return out

    def enumerate(self, start: int = 0):
        """Return an ``Iter`` of tuples containing a count (starting from ``start``) and the elements of the original ``Iter``."""
        return Iter(enumerate(self, start = start))

    def map(self, func: Callable[[T], U]) -> 'Iter[U]':
        """Return a new ``Iter``, with each element mapped under the function ``func``."""
        return Iter(map(func, self))

    def filter(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter``, containing only elements that ``func(element)`` is true for."""
        return Iter(filter(func, self))

    def skip_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        return Iter(itertools.dropwhile(func, self))

    def take_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        return Iter(itertools.takewhile(func, self))

    def permutations(self, r = None) -> 'Iter':
        return Iter(itertools.permutations(self, r = r))

    def product(self, *iters, repeat = 1) -> 'Iter':
        return Iter(itertools.product(self, *iters, repeat = repeat))

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

    def max(self):
        return max(self)

    def min(self):
        return min(self)

    def find(self, func: Callable[[T], bool]) -> Option[T]:
        for t in self:
            if func(t):
                return Some(t)

        return Nun()

    def position(self, func: Callable[[T], bool]) -> Option[int]:
        for idx, t in self:
            if func(t):
                return Some(idx)

        return Nun()

    def find_position(self, func: Callable[[T], bool]) -> Option[Tuple[int, T]]:
        for idx, t in self:
            if func(t):
                return Some((idx, t))

        return Nun()

    def reduce(self, func: Callable[[U, T], U], initial: Optional[U] = None) -> U:
        """
        Apply ``func`` cumulatively to the items in the iterable from left to right.
        The first argument of ``func`` is the accumulated value, the second is the next element of the iterable.
        If ``initial`` is given, it is first accumulated value.
        """
        return functools.reduce(func, self, initial = initial)

    # METHODS THAT DO OTHER STUFF

    def for_each(self, func: Callable[[T], None]) -> None:
        """Call a function on each element of the ``Iter``."""
        for t in self:
            func(t)
