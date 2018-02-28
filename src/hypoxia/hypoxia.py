import collections
from typing import Callable, Optional


class Panic(Exception):
    pass


class Result:
    def __init__(self, val):
        self._val = val

    def __hash__(self):
        return hash(self._val)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._val)})'

    def __eq__(self, other):
        print(self, other)
        return self.__class__ == other.__class__ and self._val == other._val


class Option:
    def __init__(self, val):
        self._val = val

    def __hash__(self):
        return hash(self._val)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._val)})'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._val == other._val


class Ok(Result):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return not self.is_ok()

    def ok(self) -> Option:
        return Some(self._val)

    def err(self) -> Option:
        return Nun()

    def map(self, func: Callable):
        return Ok(func(self._val))

    def map_err(self, func: Callable):
        return Ok(self._val)

    def and_(self, result: Result):
        return result

    def and_then(self, func: Callable):
        return Ok(func(self._val))

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
    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return not self.is_ok()

    def ok(self) -> Option:
        return Nun()

    def err(self) -> Option:
        return Some(self._val.args[0])  # the text of the exception

    def map(self, func: Callable) -> Result:
        return self

    def map_err(self, func: Callable) -> Result:
        return Err(func(self._val))

    def and_(self, result: Result):
        return self

    def and_then(self, func: Callable):
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


class Some(Option):
    def is_some(self) -> bool:
        return True

    def is_nun(self) -> bool:
        return not self.is_some()

    def unwrap(self):
        return self._val

    def unwrap_or(self, default):
        return self._val

    def unwrap_or_else(self, func: Callable):
        return self._val

    def map(self, func: Callable):
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

    def unwrap_or_else(self, func: Callable):
        return func()

    def map(self, func: Callable):
        return self


class HashMap(collections.UserDict):
    def __getitem__(self, item):
        try:
            return Some(super().__getitem__(item))
        except Exception as e:
            return Nun()

    def get(self, key):
        return super().get(key)


def open_file(file, *args, **kwargs):
    try:
        return Ok(open(file, *args, **kwargs))
    except Exception as e:
        return Err(e)
