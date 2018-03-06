import pytest

from hypoxia import HashMap


@pytest.fixture(scope = 'function')
def hashmap():
    h = HashMap(num = 2, foo = 'bar')

    return h


def test_get_then_map_then_unwrap_or_with_some(hashmap):
    assert hashmap.get('num').map(lambda x: x ** 2).unwrap_or(0) == 4


def test_get_then_map_then_unwrap_or_with_nun(hashmap):
    assert hashmap.get('notnum').map(lambda x: x ** 2).unwrap_or(0) == 0
