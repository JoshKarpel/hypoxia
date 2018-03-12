import pytest

from hypoxia import Dwell


@pytest.fixture(scope = 'function')
def char_dwell():
    return Dwell(c for c in 'Hello world!')


@pytest.fixture(scope = 'function')
def int_dwell():
    return Dwell(range(5))


def test_map_returns_dwell(char_dwell):
    assert type(char_dwell.map(lambda c: c.upper())) == Dwell


def test_map_doubler(int_dwell):
    assert tuple(int_dwell.map(lambda x: 2 * x)) == (0, 2, 4, 6, 8)


def test_filter_returns_dwell(char_dwell):
    assert type(char_dwell.filter(lambda c: c != 'l')) == Dwell


def test_filter_evens(int_dwell):
    assert tuple(int_dwell.filter(lambda x: x % 2 == 0)) == (0, 2, 4)


def test_all_true(int_dwell):
    assert int_dwell.map(lambda x: x < 10).all()


def test_all_false(int_dwell):
    assert not int_dwell.map(lambda x: x > 3).all()


def test_any_true(int_dwell):
    assert int_dwell.map(lambda x: x == 0).any()


def test_any_false(int_dwell):
    assert not int_dwell.map(lambda x: x < 0).any()
