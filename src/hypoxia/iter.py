from typing import Iterable, Callable, Generic, TypeVar, Tuple, Optional, Iterator, Union, List, Any, Type, Collection
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
        """Return an ``Iter`` that "counts" forever from ``start`` by ``step`` increments."""
        return cls(itertools.count(start = start, step = step))

    @classmethod
    def repeat(cls, element: T, times: Optional[int] = None) -> 'Iter[T]':
        """Return an ``Iter`` that yields ``element`` a certain number of ``times``, or forever if ``times`` is ``None``."""
        if times is None:
            return cls(itertools.repeat(element))
        return cls(itertools.repeat(element, times = times))

    # METHODS THAT RETURN NEW ITERATORS

    def chain(self, *iters) -> 'Iter':
        """Return a new ``Iter`` that yields all of the elements of the component iterators."""
        return self.__class__(itertools.chain(self, *iters))

    def __add__(self, other):
        """Operator overload for ``Iter.chain``."""
        return self.chain(other)

    def zip(self, *iters: Iterable) -> 'Iter[Tuple]':
        """Make an ``Iter`` of tuples of aligned elements from this ``Iter`` and each of the input iterables."""
        return self.__class__(zip(self, *iters))

    def __and__(self, other):
        """Operator overload for ``Iter.zip``."""
        return self.zip(other)

    def zip_longest(self, *iters: Iterable, fill = None) -> 'Iter[Tuple]':
        """
        Make an ``Iter`` of tuples of aligned elements from this ``Iter`` and each of the input iterables.
        Instead of stopping at the end of the shortest iterable, this method continues yielding tuples, using the ``fill`` value to replace missing inputs.
        """
        return self.__class__(itertools.zip_longest(self, *iters, fillvalue = fill))

    def __or__(self, other):
        """Operator oeverload for ``Iter.zip_longest``."""
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
        """Return a new ``Iter`` with each element mapped under the function ``func``."""
        return self.__class__(map(func, self))

    def star_map(self, func: Callable[[Any], U]) -> 'Iter[U]':
        """
        Return a new ``Iter`` with each element mapped under the function ``func``.
        Each element is unpacked into the function's arguments.
        """
        return self.__class__(itertools.starmap(func, self))

    def filter(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter`` containing only elements that ``func(element)`` is true for."""
        return self.__class__(filter(func, self))

    def filter_map(self, func: Callable[[T], Option[U]]) -> 'Iter[U]':
        """Return a new ``Iter`` containing the values of ``func(element)`` if ``func(element)`` is :class:`Some` and skipping it otherwise."""
        return self.map(func).filter(lambda x: x.is_some()).map(lambda x: x.unwrap())

    def compress(self, selectors: Iterable[bool]) -> 'Iter[T]':
        """Return a new ``Iter`` containing only the elements where ``selector`` has a ``True``-like value at that index."""
        return self.__class__(itertools.compress(self, selectors))

    def skip_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter`` containing all of the elements after (and including) the first element that ``func(element)`` is ``False`` for."""
        return self.__class__(itertools.dropwhile(func, self))

    def take_while(self, func: Callable[[T], bool]) -> 'Iter[T]':
        """Return a new ``Iter`` containing all of the elements up to the last one that ``func(element)`` is ``True`` for."""
        return self.__class__(itertools.takewhile(func, self))

    def product(self, *iters, repeat: int = 1) -> 'Iter':
        """Return a new ``Iter`` containing the Cartesian product of the ``Iter`` and the iterables in ``iter``."""
        return self.__class__(itertools.product(self, *iters, repeat = repeat))

    def __mul__(self, other):
        """Operator overload for ``Iter.product``."""
        return self.product(other)

    def permutations(self, r = None) -> 'Iter':
        """Return a new ``Iter`` containing all of the permutations of the elements of the ``Iter`` of length ``r``."""
        return self.__class__(itertools.permutations(self, r = r))

    def combinations(self, r) -> 'Iter':
        """Return a new ``Iter`` containing all of the combinations of the elements of the ``Iter`` of length ``r``."""
        return self.__class__(itertools.combinations(self, r))

    def combinations_with_replacement(self, r) -> 'Iter':
        """Return a new ``Iter`` containing all of the combinations of the elements of the ``Iter`` of length ``r``, with replacement."""
        return self.__class__(itertools.combinations_with_replacement(self, r))

    def cycle(self):
        """Return a new ``Iter`` which repeats the elements of the ``Iter`` cyclically., forever."""
        return self.__class__(itertools.cycle(self))

    def sorted(self, key = None, reversed = False):
        """
        Return a new ``Iter`` containing the elements of the ``Iter`` in sorted order.
        ``key`` and ``reversed`` have the same meaning as in :function:`sorted`.
        """
        return Iter(sorted(self, key = key, reverse = reversed))

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
        """Return the maximum value in the ``Iter``, possibly using a ``key`` function."""
        if key is None:
            return max(self)
        return max(self, key = key)

    def min(self, key = None):
        """Return the minimum value in the ``Iter``, possibly using a ``key`` function."""
        if key is None:
            return min(self)
        return min(self, key = key)

    def sum(self, start: Optional[T] = None) -> T:
        """Return the sum of the elements in the ``Iter``, possibly using a ``start`` value."""
        if start is None:
            return sum(self)
        return sum(self, start)

    def mul(self, initial: U = 1) -> U:
        """Fold the ``Iter`` via pairwise multiplication."""
        return self.reduce(operator.mul, initial = initial)

    def dot(self, other):
        """Return the dot product of two ``Iter``s (sum of elementwise product)."""
        return sum(map(operator.mul, self, other))

    def __matmul__(self, other):
        """Operator overload for ``Iter.dot``."""
        return self.dot(other)

    def find(self, func: Callable[[T], bool]) -> Option[T]:
        """Returns ``Some(element)``, for the first ``element`` of the ``Iter`` where ``func(element)`` is ``True`."""
        for t in self:
            if func(t):
                return Some(t)

        return Nun()

    def position(self, func: Callable[[T], bool]) -> Option[int]:
        """Returns ``Some(index)``, for the first ``index`` of the ``Iter`` where ``func(element)`` is ``True`."""
        for idx, t in self.enumerate():
            if func(t):
                return Some(idx)

        return Nun()

    def find_position(self, func: Callable[[T], bool]) -> Option[Tuple[int, T]]:
        """Returns ``Some(index, element)``, for the first ``element`` of the ``Iter`` where ``func(element)`` is ``True`."""
        for idx, t in self.enumerate():
            if func(t):
                return Some((idx, t))

        return Nun()

    def reduce(self, func: Callable[[U, T], U], initial: Optional[U] = None) -> U:
        """
        Apply ``func`` cumulatively to the items in the iterable from left to right.
        The first argument of ``func`` is the accumulated value, the second is the next element of the iterable.
        If ``initial`` is given, it is first accumulated value.
        """
        if initial is None:
            return functools.reduce(func, self)
        return functools.reduce(func, self, initial)

    def collect(self, collection_type: Type[Collection]) -> Collection[T]:
        """Collect the elements of the ``Iter`` into a collection of type ``collection_type``."""
        return collection_type(self)

    def join(self, separator: str = ''):
        """Join the elements of the ``Iter``, as a string join with separation ``separator``."""
        return separator.join(self.map(str))

    # METHODS THAT DO OTHER STUFF

    def partition(self, func: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
        """
        Divides the ``Iter`` elements into two groups based on whether ``func(element)`` is ``True`` or ``False``.
        Returns a tuple of two lists, the first with all of the ``True`` elements, the second with all of the ``False`` elements.
        """
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
        """Call a function on each element of the ``Iter``, unpacking each element into the function's arguments as a tuple."""
        for t in self:
            func(*t)
