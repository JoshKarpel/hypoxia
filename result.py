from typing import Callable, Optional


class Panic(Exception):
    pass


class Result:
    def __init__(self, val):
        self._val = val

    def __hash__(self):
        return hash(self._val)


class Option:
    def __init__(self, val):
        self._val = val

    def __hash__(self):
        return hash(self._val)


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

    def unwrap_or_default(self):
        return self


class Err(Result):
    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return not self.is_ok()

    def ok(self) -> Option:
        return Nun()

    def err(self) -> Option:
        return Some(self._val)

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

    def unwrap_or_default(self):
        raise NotImplementedError  # ick


class Some(Option):
    pass


class Nun(Option):
    def __init__(self):
        super().__init__(None)
