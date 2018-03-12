import pytest

from hypoxia import Iter


@pytest.fixture(scope = 'function')
def char_iter():
    return Iter(c for c in 'Hello world!')


@pytest.fixture(scope = 'function')
def int_iter():
    return Iter(range(5))


def test_zip(char_iter, int_iter):
    assert tuple(int_iter.zip(char_iter)) == ((0, 'H'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o'))


def test_enumerate():
    d = Iter(('a', 'b', 'c'))

    assert tuple(d.enumerate()) == ((0, 'a'), (1, 'b'), (2, 'c'))


def test_map_returns_iter(char_iter):
    assert type(char_iter.map(lambda c: c.upper())) == Iter


def test_map_doubler(int_iter):
    assert tuple(int_iter.map(lambda x: 2 * x)) == (0, 2, 4, 6, 8)


def test_filter_returns_iter(char_iter):
    assert type(char_iter.filter(lambda c: c != 'l')) == Iter


def test_filter_evens(int_iter):
    assert tuple(int_iter.filter(lambda x: x % 2 == 0)) == (0, 2, 4)


def test_all_true(int_iter):
    assert int_iter.map(lambda x: x < 10).all()


def test_all_false(int_iter):
    assert not int_iter.map(lambda x: x > 3).all()


def test_any_true(int_iter):
    assert int_iter.map(lambda x: x == 0).any()


def test_any_false(int_iter):
    assert not int_iter.map(lambda x: x < 0).any()


def test_on_list():
    d = Iter([0, 1, 2, 3, 4])

    assert tuple(d.map(lambda x: 2 * x)) == (0, 2, 4, 6, 8)
