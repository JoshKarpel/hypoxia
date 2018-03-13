from typing import Iterable, Callable, Generic, TypeVar, Tuple, Optional, Iterator, Union, List, Any, Type, Container
import functools
import itertools
import operator

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

    # CONSTRUCTORS

    @classmethod
    def count(cls, start = 0, step = 1) -> 'Iter[int]':
        return cls(itertools.count(start = start, step = step))

    @classmethod
    def repeat(cls, element: T, times: Optional[int] = None) -> 'Iter[T]':
        if times is None:
            return cls(itertools.repeat(element))
        return cls(itertools.repeat(element, times = times))

    # METHODS THAT RETURN NEW ITERATORS

    def chain(self, *iters) -> 'Iter':
        return self.__class__(itertools.chain(self, *iters))

    def __add__(self, other):
        return self.chain(other)

    def zip(self, *iters: Iterable) -> 'Iter[Tuple]':
        """Make an ``Iter`` of tuples of aligned elements from this ``Iter`` and each of the input iterables."""
        return self.__class__(zip(self, *iters))

    def __and__(self, other):
        return self.zip(other)

    def zip_longest(self, *iters: Iterable, fill = None) -> 'Iter[Tuple]':
        return self.__class__(itertools.zip_longest(self, *iters, fillvalue = fill))

    def __or__(self, other):
        return self.zip_longest(other)

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
        return self.__class__(enumerate(self, start = start))

    def map(self, func: Callable[[T], U]) -> 'Iter[U]':
        """Return a new ``Iter``, with each element mapped under the function ``func``."""
        return self.__class__(map(func, self))

    def star_map(self, func: Callable[[Any], U]) -> 'Iter[U]':
        return self.__class__(itertools.starmap(func, self))

    def filter(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter``, containing only elements that ``func(element)`` is true for."""
        return self.__class__(filter(func, self))

    def filter_map(self, func: Callable[[T], Option[U]]) -> 'Iter[U]':
        return self.map(func).filter(lambda x: x.is_some()).map(lambda x: x.unwrap())

    def compress(self, selectors: Iterable[bool]) -> 'Iter[T]':
        return self.__class__(itertools.compress(self, selectors))

    def skip_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        return self.__class__(itertools.dropwhile(func, self))

    def take_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        return self.__class__(itertools.takewhile(func, self))

    def permutations(self, r = None) -> 'Iter':
        return self.__class__(itertools.permutations(self, r = r))

    def combinations(self, r) -> 'Iter':
        return self.__class__(itertools.combinations(self, r))

    def combinations_with_replacement(self, r) -> 'Iter':
        return self.__class__(itertools.combinations_with_replacement(self, r))

    def product(self, *iters, repeat: int = 1) -> 'Iter':
        return self.__class__(itertools.product(self, *iters, repeat = repeat))

    def __mul__(self, other):
        return self.product(self, other)

    def cycle(self):
        return self.__class__(itertools.cycle(self))

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

    def max(self, key = None):
        return max(self, key = key)

    def min(self, key = None):
        return min(self, key = key)

    def sum(self):
        return sum(self)

    def mul(self, initial: U = 1) -> U:
        return self.reduce(operator.mul, initial = initial)

    def dot(self, other):
        return sum(map(operator.mul, self, other))

    def __matmul__(self, other):
        return self.dot(other)

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

    def collect(self, collection_type: Type[Container]) -> Container[T]:
        return collection_type(self)

    # METHODS THAT DO OTHER STUFF

    def partition(self, func: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
        passed = []
        failed = []
        for t in self:
            if func(t):
                passed.append(t)
            else:
                failed.append(t)

        return passed, failed

    def for_each(self, func: Callable[[T], None]) -> None:
        """Call a function on each element of the ``Iter``."""
        for t in self:
            func(t)

    def star_for_each(self, func: Callable[[Any], None]) -> None:
        for t in self:
            func(*t)

    def sorted(self, key = None, reverse = False):
        return sorted(self, key = key, reverse = reverse)
