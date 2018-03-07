import pytest

from hypoxia import HashMap


@pytest.fixture(scope = 'function')
def hashmap():
    h = HashMap(num = 2, foo = 'bar')

    return h


def test_indexing_and_getting(hashmap):
    for key in hashmap:
        assert hashmap[key] == hashmap.get(key)  # Somes at this point
        assert hashmap[key] is not hashmap.get(key)  # because wrapped in Some
        assert hashmap[key].unwrap() is hashmap.get(key).unwrap()


def test_get_then_map_then_unwrap_or_with_some(hashmap):
    assert hashmap.get('num').map(lambda x: x ** 2).unwrap_or(0) == 4


def test_get_then_map_then_unwrap_or_with_nun(hashmap):
    assert hashmap.get('notnum').map(lambda x: x ** 2).unwrap_or(0) == 0


def test_setting_works(hashmap):
    hashmap['new'] = 'newval'

    assert hashmap['new'].unwrap() == 'newval'


def test_inserting_works(hashmap):
    hashmap.insert('new', 'newval')

    assert hashmap['new'].unwrap() == 'newval'
