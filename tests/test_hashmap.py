import pytest

from hypoxia import HashMap


@pytest.fixture(scope = 'function')
def hashmap():
    h = HashMap(num = 2, foo = 'bar')

    return h


def test_indexing_equals_getting(hashmap):
    for key in hashmap:
        assert hashmap[key] == hashmap.get(key)


def test_indexing_not_is_getting(hashmap):
    for key in hashmap:
        assert hashmap[key] is not hashmap.get(key)  # not actually the same object


def test_get_then_map_then_unwrap_or_with_some(hashmap):
    assert hashmap.get('num').map(lambda x: x ** 2).unwrap_or(0) == 4


def test_get_then_map_then_unwrap_or_with_nun(hashmap):
    assert hashmap.get('notnum').map(lambda x: x ** 2).unwrap_or(0) == 0


def test_assignment_works(hashmap):
    hashmap['new'] = 'newval'

    assert hashmap['new'].unwrap() == 'newval'
