import abc
from typing import Callable, Any

from hypoxia import Panic


class Option(abc.ABC):
    def __init__(self, val):
        self._val = val

    def __hash__(self):
        return hash(self._val)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._val)})'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val == other._val

    @abc.abstractmethod
    def is_some(self) -> bool:
        return True

    @abc.abstractmethod
    def is_nun(self) -> bool:
        return False

    @abc.abstractmethod
    def unwrap(self):
        return self._val

    @abc.abstractmethod
    def unwrap_or(self, default):
        return self._val

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable[[], 'Option']):
        return self._val

    @abc.abstractmethod
    def map(self, func: Callable[[Any], 'Option']):
        return Some(func(self._val))


class Some(Option):
    def is_some(self) -> bool:
        return True

    def is_nun(self) -> bool:
        return False

    def unwrap(self):
        return self._val

    def unwrap_or(self, default):
        return self._val

    def unwrap_or_else(self, func: Callable[[], Option]):
        return self._val

    def map(self, func: Callable[[Any], Option]):
        return Some(func(self._val))


class Nun(Option):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'Nun'

    def is_some(self) -> bool:
        return False

    def is_nun(self) -> bool:
        return not self.is_some()

    def unwrap(self):
        raise Panic('unwrapped Nun')

    def unwrap_or(self, default):
        return default

    def unwrap_or_else(self, func: Callable[[], Option]):
        return func()

    def map(self, func: Callable[[Any], Option]):
        return self
