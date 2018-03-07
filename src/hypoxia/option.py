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
        """Returns ``True`` if the ``Option`` is a ``Some``, and ``False`` if it is a ``Nun``."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_nun(self) -> bool:
        """Returns ``True`` if the ``Option`` is a ``Nun``, and ``False`` if it is a ``Some``."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self):
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, this raises a :class:`Panic`."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or(self, default):
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, return ``default`` instead."""
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable[[], 'Option']):
        """If the ``Option`` is a ``Some``, return its value. If it is a ``Nun``, return ``func()``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, func: Callable[[Any], 'Option']):
        """If the ``Option`` is a ``Some``, return ``Some(func(value))``. If it is a ``Nun``, return ``Nun``."""
        raise NotImplementedError

    @abc.abstractmethod
    def map_or(self, func: Callable[[Any], Any], default: Any):
        raise NotImplementedError


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

    def map_or(self, func: Callable[[Any], Any], default: Any):
        return func(self._val)


class Nun(Option):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'Nun'

    def is_some(self) -> bool:
        return False

    def is_nun(self) -> bool:
        return True

    def unwrap(self):
        raise Panic('unwrapped Nun')

    def unwrap_or(self, default):
        return default

    def unwrap_or_else(self, func: Callable[[], Option]):
        return func()

    def map(self, func: Callable[[Any], Option]):
        return self

    def map_or(self, func: Callable[[Any], Any], default: Any):
        return default
