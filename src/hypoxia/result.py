import abc
from typing import Callable, Any

from hypoxia import Panic
from .option import Option, Some, Nun


class Result(abc.ABC):
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
        raise NotImplementedError

    @abc.abstractmethod
    def is_err(self) -> bool:
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
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or(self, optb):
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable):
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self):
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_err(self):
        raise NotImplementedError


class Ok(Result):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> Option:
        return Some(self._val)

    def err(self) -> Option:
        return Nun()

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

    def unwrap_or(self, optb):
        return self

    def unwrap_or_else(self, func: Callable):
        return func(self._val)

    def unwrap(self):
        return self._val

    def unwrap_err(self):
        raise Panic(f'unwrap_err on Ok({self._val})')


class Err(Result):
    def __init__(self, val):
        if not isinstance(val, Exception):
            raise Panic(f'Err value must be an exception, but was {val}')

        super().__init__(val)

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> Option:
        return Nun()

    def err(self) -> Option:
        return Some(self._val.args[0])  # the text of the exception

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

    def unwrap_or(self, optb):
        return optb

    def unwrap_or_else(self, func: Callable):
        return func(self._val)

    def unwrap(self):
        raise self._val

    def unwrap_err(self):
        return self._val

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val.__class__ == other._val.__class__ and self._val.args == other._val.args
