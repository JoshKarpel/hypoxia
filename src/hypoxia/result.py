import abc
from typing import Callable, Any, TypeVar, Generic

from .exceptions import Panic
from . import option

T = TypeVar('T')
U = TypeVar('U')


class Result(abc.ABC, Generic[T]):
    """
    The value inside an ``Err`` must be something that counts as an instance of :class:`Exception`.
    """

    def __init__(self, val):
        self._val = val

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
    def ok(self) -> 'Option':
        raise NotImplementedError

    @abc.abstractmethod
    def err(self) -> 'Option':
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, func: Callable):
        raise NotImplementedError

    @abc.abstractmethod
    def map_err(self, func: Callable[[Any], 'Result']):
        raise NotImplementedError

    @abc.abstractmethod
    def and_(self, result: 'Result'):
        raise NotImplementedError

    @abc.abstractmethod
    def and_then(self, func: Callable[[Any], 'Result']):
        raise NotImplementedError

    @abc.abstractmethod
    def or_(self, result: 'Result'):
        raise NotImplementedError

    @abc.abstractmethod
    def or_else(self, func: Callable):
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self):
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or(self, default):
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, return ``default`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable):
        """If the ``Result`` is an ``Ok``, return its value. If it is a ``Err``, return ``func(value)`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_err(self):
        """If the ``Result`` is an ``Err``, return its value. If it is a ``Ok``, this raises a :class:`Panic`."""
        raise NotImplementedError


class Ok(Result):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> option.Option:
        return option.Some(self._val)

    def err(self) -> option.Option:
        return option.Nun()

    def map(self, func: Callable):
        return Ok(func(self._val))

    def map_err(self, func: Callable[[Any], Result]):
        return self

    def and_(self, result: Result):
        return result

    def and_then(self, func: Callable[[Any], Result]):
        return func(self._val)

    def or_(self, result: Result):
        return self

    def or_else(self, func: Callable):
        return self

    def unwrap(self):
        return self._val

    def unwrap_or(self, default):
        return self._val

    def unwrap_or_else(self, func: Callable):
        return self._val

    def unwrap_err(self):
        raise Panic(f'unwrap_err on {self}')


class Err(Result):
    def __init__(self, val):
        if not isinstance(val, Exception):
            raise Panic(f'Err value must be an exception, but was {val}')

        super().__init__(val)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val.__class__ == other._val.__class__ and self._val.args == other._val.args

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> option.Option:
        return option.Nun()

    def err(self) -> option.Option:
        return option.Some(self._val.args[0])  # the text of the exception

    def map(self, func: Callable[[Any], Result]) -> Result:
        return self

    def map_err(self, func: Callable[[Any], Result]) -> Result:
        return func(self._val)

    def and_(self, result: Result):
        return self

    def and_then(self, func: Callable[[Any], Result]):
        return self

    def or_(self, result: Result):
        return result

    def or_else(self, func: Callable):
        return func(self._val)

    def unwrap(self):
        raise Panic(f'unwrap on {self}')

    def unwrap_or(self, default):
        return default

    def unwrap_or_else(self, func: Callable):
        return func(self._val)

    def unwrap_err(self):
        return self._val
