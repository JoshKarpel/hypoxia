import collections

from .option import Some, Nun


class HashMap(collections.UserDict):
    def __getitem__(self, item):
        try:
            return Some(super().__getitem__(item))
        except KeyError:
            return Nun()

    def get(self, key):
        return super().get(key)
