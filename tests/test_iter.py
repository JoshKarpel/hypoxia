import pytest

from hypoxia import Iter, Some, Nun


@pytest.fixture(scope = 'function')
def char_iter():
    return Iter(c for c in 'Hello world!')


@pytest.fixture(scope = 'function')
def int_iter():
    return Iter(range(5))


def test_zip(char_iter, int_iter):
    x = int_iter.zip(char_iter)
    assert list(x) == [(0, 'H'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o')]


def test_and(char_iter, int_iter):
    x = int_iter & char_iter
    assert list(x) == [(0, 'H'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o')]


def test_unzip():
    foo = Iter(range(3)).zip(range(3), range(3))

    a, b, c = foo.unzip()

    assert a == b == c == [0, 1, 2]


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


def test_count():
    count = Iter.count(start = 5, step = 2)

    assert next(count) == 5
    assert next(count) == 7
    assert next(count) == 9
    assert next(count) == 11


def test_repeat():
    repeat = Iter.repeat(True)

    for _ in range(100):
        assert next(repeat)


def test_repeat_limit():
    repeat = Iter.repeat(True, 10)

    assert list(repeat) == [True for _ in range(10)]


def test_chain(char_iter, int_iter):
    x = char_iter.chain(int_iter)

    assert list(x) == ['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', 0, 1, 2, 3, 4]


def test_add(char_iter, int_iter):
    x = char_iter + int_iter

    assert list(x) == ['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', 0, 1, 2, 3, 4]


def test_zip_longest():
    x = Iter(range(3)).zip_longest(range(2))

    assert list(x) == [(0, 0), (1, 1), (2, None)]


def test_zip_longest_other_way():
    x = Iter(range(2)).zip_longest(range(3))

    assert list(x) == [(0, 0), (1, 1), (None, 2)]


def test_or():
    x = Iter(range(3)) | range(2)

    assert list(x) == [(0, 0), (1, 1), (2, None)]


def test_star_map():
    def pow(x, y):
        return x ** y

    x = Iter(range(4)).zip(range(4)).star_map(pow)

    assert list(x) == [0 ** 0, 1 ** 1, 2 ** 2, 3 ** 3]


def test_filter_map(int_iter):
    def fm(x):
        if x % 2 == 0:
            return Some(x ** 2)
        else:
            return Nun()

    x = int_iter.filter_map(fm)

    assert list(x) == [0, 4, 16]


def test_compress():
    x = Iter('hello!')
    selectors = [0, 1, 0, 1, 1, 0]

    assert ''.join(x.compress(selectors)) == 'elo'
