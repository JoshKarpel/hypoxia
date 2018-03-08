import abc
from typing import Callable, Any, TypeVar, Generic

from .exceptions import Panic
from . import result

T = TypeVar('T')
U = TypeVar('U')


class Option(abc.ABC, Generic[T]):
    def __init__(self, val: T):
        self._val = val

    def __hash__(self):
        return hash(self._val)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._val)})'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val == other._val

    def __iter__(self):
        yield self._val

    @abc.abstractmethod
    def is_some(self) -> bool:
        """Returns ``True`` if the ``Option`` is a ``Some``, and ``False`` if it is a ``Nun``."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_nun(self) -> bool:
        """Returns ``True`` if the ``Option`` is a ``Nun``, and ``False`` if it is a ``Some``."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self) -> T:
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or(self, default: T) -> T:
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, return ``default`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, return ``func()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, func: Callable[[T], U]) -> 'Option[U]':
        """If the ``Option`` is a ``Some``, return ``Some(func(value))``. If it is a ``Nun``, return ``Nun()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map_or(self, func: Callable[[T], U], default: U) -> U:
        """If the ``Option`` is a ``Some``, return ``func(value)``. If it is a ``Nun``, return ``default``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map_or_else(self, func: Callable[[T], U], default_func: Callable[[], U]) -> U:
        """If the ``Option`` is a ``Some``, return ``func(value)``. If it is a ``Nun``, return ``default_func()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def ok_or(self, err: Exception) -> 'result.Result[T]':
        """If the ``Option`` is a ``Some``, return ``Ok(value)``. If it is a ``Nun``, return ``Err(err)``."""
        raise NotImplementedError

    @abc.abstractmethod
    def ok_or_else(self, err_func: Callable[[], Exception]) -> 'result.Result[T]':
        """If the ``Option`` is a ``Some``, return ``Ok(value)``. If it is a ``Nun``, return ``Err(err())``."""
        raise NotImplementedError

    @abc.abstractmethod
    def and_(self, other: 'Option[U]') -> 'Option[U]':
        """If either ``Option`` is ``Nun``, return ``Nun``. If both are ``Some``, return ``other``."""
        raise NotImplementedError

    @abc.abstractmethod
    def and_then(self, func: Callable[[], U]) -> 'Option[U]':
        """If the ``Option`` is a ``Some``, return ``func()``. If it is a ``Nun``, return ``Nun()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def or_(self, other: 'Option[T]') -> 'Option[T]':
        """If the ``Option`` is a ``Some``, return it. If it is a ``Nun``, return ``other``."""
        raise NotImplementedError

    @abc.abstractmethod
    def or_else(self, func: Callable[[], T]) -> 'Option[T]':
        """If the ``Option`` is a ``Some``, return it. If it is a ``Nun``, return ``func()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_or_insert(self, value: T) -> T:
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, convert this ``Option`` into ``Some(value)`` and return the value."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_or_insert_with(self, func: Callable[[], T]) -> T:
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, convert this ``Option`` into ``Some(func())`` and return the value."""
        raise NotImplementedError


class Some(Option):
    def is_some(self) -> bool:
        return True

    def is_nun(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._val

    def unwrap_or(self, default: T) -> T:
        return self._val

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self._val

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return Some(func(self._val))

    def map_or(self, func: Callable[[T], U], default: U) -> U:
        return func(self._val)

    def map_or_else(self, func: Callable[[T], U], default_func: Callable[[], U]) -> U:
        return func(self._val)

    def ok_or(self, err: Exception) -> 'result.Result[T]':
        return result.Ok(self._val)

    def ok_or_else(self, err_func: Callable[[], Exception]) -> 'result.Result[T]':
        return result.Ok(self._val)

    def and_(self, other: 'Option[U]') -> 'Option[U]':
        if other.is_some():
            return other
        return Nun()

    def and_then(self, func: Callable[[T], U]) -> 'Option[U]':
        return Some(func(self._val))

    def or_(self, other: 'Option[T]') -> 'Option[T]':
        return self

    def or_else(self, func: Callable[[], T]) -> 'Option[T]':
        return self

    def get_or_insert(self, value: T) -> T:
        return self._val

    def get_or_insert_with(self, func: Callable[[], T]) -> T:
        return self._val


class Nun(Option):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'Nun'

    def __iter__(self):
        """This produces an empty iterator."""
        for _ in []:
            yield

    def is_some(self) -> bool:
        return False

    def is_nun(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise Panic('unwrapped Nun')

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return func()

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return self

    def map_or(self, func: Callable[[T], U], default: U) -> U:
        return default

    def map_or_else(self, func: Callable[[T], U], default_func: Callable[[], U]) -> U:
        return default_func()

    def ok_or(self, err: Exception) -> 'result.Result[T]':
        return result.Err(err)

    def ok_or_else(self, err_func: Callable[[], Exception]) -> 'result.Result[T]':
        return result.Err(err_func())

    def and_(self, other: 'Option[U]') -> 'Option[U]':
        return Nun()

    def and_then(self, func: Callable[[], U]) -> 'Option[U]':
        return Nun()

    def or_(self, other: 'Option[T]') -> 'Option[T]':
        return other

    def or_else(self, func: Callable[[], T]) -> 'Option[T]':
        return Some(func())

    def get_or_insert(self, value: T) -> T:
        self.__class__ = Some
        self._val = value

        return self._val

    def get_or_insert_with(self, func: Callable[[], T]) -> T:
        self.__class__ = Some
        self._val = func()

        return self._val
