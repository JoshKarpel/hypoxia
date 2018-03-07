from typing import Hashable, Any

import collections

from .option import Option, Some, Nun


class HashMap(collections.UserDict):
    def __getitem__(self, item: Hashable) -> Option:
        try:
            return Some(super().__getitem__(item))
        except KeyError:
            return Nun()

    def get(self, key: Hashable) -> Option:
        return super().get(key)

    def insert(self, key: Hashable, item: Any):
        self.__setitem__(key, item)
