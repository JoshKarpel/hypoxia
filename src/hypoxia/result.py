import abc
from typing import Callable, TypeVar, Generic, Union

from .exceptions import Panic
from . import option

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
F = TypeVar('F')


class Result(abc.ABC, Generic[T, E]):
    """
    The value inside an ``Err`` must be something that counts as an instance of :class:`Exception`.
    """

    def __init__(self, value: Union[T, E]):
        self._val = value

    def __hash__(self):
        return hash(self._val)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._val)})'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val == other._val

    @abc.abstractmethod
    def is_ok(self) -> bool:
        """Returns ``True`` if the ``Result`` is an ``Ok``, and ``False`` if it is an ``Err``."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_err(self) -> bool:
        """Returns ``True`` if the ``Result`` is an ``Err``, and ``False`` if it is an ``Ok``."""
        raise NotImplementedError

    @abc.abstractmethod
    def ok(self) -> 'option.Option[T]':
        """Returns ``Some(value)`` if the ``Result`` is an ``Ok``, and ``Nun`` if it is an ``Err``."""
        raise NotImplementedError

    @abc.abstractmethod
    def err(self) -> 'option.Option[E]':
        """Returns ``Some(value)`` if the ``Result`` is an ``Err``, and ``Nun`` if it is an ``Err``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, func: Callable[[T], U]) -> 'Result[U, E]':
        raise NotImplementedError

    @abc.abstractmethod
    def map_err(self, func: Callable[[E], F]) -> 'Result[T, F]':
        raise NotImplementedError

    @abc.abstractmethod
    def and_(self, result: 'Result[T, E]'):
        raise NotImplementedError

    @abc.abstractmethod
    def and_then(self, func: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        raise NotImplementedError

    @abc.abstractmethod
    def or_(self, result: 'Result[T, F]') -> 'Result[T, F]':
        raise NotImplementedError

    @abc.abstractmethod
    def or_else(self, func: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self) -> T:
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or(self, default: T) -> T:
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, return ``default`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, return ``func(value)`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """If the ``Result`` is an ``Err``, return its value. If it is a ``Ok``, this raises a :class:`Panic`."""
        raise NotImplementedError


class Ok(Result):
    def __iter__(self):
        yield self._val

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> 'option.Option[T]':
        return option.Some(self._val)

    def err(self) -> 'option.Option[E]':
        return option.Nun()

    def map(self, func: Callable[[T], U]) -> 'Result[U, E]':
        return Ok(func(self._val))

    def map_err(self, func: Callable[[E], F]) -> 'Result[T, F]':
        return self

    def and_(self, result: 'Result[T, E]'):
        return result

    def and_then(self, func: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        return func(self._val)

    def or_(self, result: 'Result[T, F]') -> 'Result[T, F]':
        return self

    def or_else(self, func: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        return self

    def unwrap(self) -> T:
        return self._val

    def unwrap_or(self, default: T) -> T:
        return self._val

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return self._val

    def unwrap_err(self) -> E:
        raise Panic(f'unwrap_err on {self}')


class Err(Result):
    def __init__(self, value):
        if not isinstance(value, Exception):
            raise Panic(f'Err value must be an exception, but was {value}')

        super().__init__(value)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val.__class__ == other._val.__class__ and self._val.args == other._val.args

    def __hash__(self):
        return hash((self._val.__class__, self._val.args))

    def __iter__(self):
        """This produces an empty iterator."""
        for _ in []:
            yield

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> 'option.Option[T]':
        return option.Nun()

    def err(self) -> 'option.Option[E]':
        return option.Some(self._val.args[0])  # the text of the exception

    def map(self, func: Callable[[T], U]) -> 'Result[U, E]':
        return self

    def map_err(self, func: Callable[[E], F]) -> 'Result[T, F]':
        return func(self._val)

    def and_(self, result: 'Result[T, E]'):
        return self

    def and_then(self, func: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        return self

    def or_(self, result: 'Result[T, F]') -> 'Result[T, F]':
        return result

    def or_else(self, func: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        return func(self._val)

    def unwrap(self) -> T:
        raise Panic(f'unwrap on {self}')

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return func(self._val)

    def unwrap_err(self) -> E:
        return self._val
