import pytest

from hypoxia import Iter, Some, Nun

HELLO_WORLD = 'Hello world!'


@pytest.fixture(scope = 'function')
def char_iter():
    return Iter(c for c in HELLO_WORLD)


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


def test_reduce(int_iter):
    assert int_iter.reduce(lambda acc, elem: max(acc, elem)) == 4


def test_reduce_with_initial(int_iter):
    assert int_iter.reduce(lambda acc, elem: max(acc, elem), initial = 10) == 10


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


def test_partition(int_iter):
    even, odd = int_iter.partition(lambda x: x % 2 == 0)

    assert even == [0, 2, 4]
    assert odd == [1, 3]


def test_for_each(int_iter, mocker):
    mock = mocker.MagicMock()

    int_iter.for_each(mock)

    assert mock.call_count == 5
    assert mock.call_args_list == [((x,),) for x in range(5)]


def test_start_for_each(char_iter, int_iter, mocker):
    mock = mocker.MagicMock()

    char_iter.zip(int_iter).star_for_each(mock)

    assert mock.call_count == 5
    assert mock.call_args_list == [(('H', 0),), (('e', 1),), (('l', 2),), (('l', 3),), (('o', 4),)]


def test_max(int_iter):
    assert int_iter.max() == 4


def test_max_by_key(int_iter):
    assert int_iter.max(lambda x: -x) == 0


def test_min(int_iter):
    assert int_iter.min() == 0


def test_min_by_key(int_iter):
    assert int_iter.min(lambda x: -x) == 4


def test_sum(int_iter):
    assert int_iter.sum() == 1 + 2 + 3 + 4


def test_sum_with_start(int_iter):
    assert int_iter.sum(start = 5) == 5 + 1 + 2 + 3 + 4


def test_mul(int_iter):
    next(int_iter)  # skip 0
    assert int_iter.mul() == 2 * 3 * 4


def test_mul_with_initial(int_iter):
    next(int_iter)  # skip 0
    assert int_iter.mul(initial = 5) == 2 * 3 * 4 * 5


def test_dot():
    a = Iter(range(3))
    b = Iter(range(4))

    return a.dot(b) == 1 ** 2 + 2 ** 2 + 3 ** 2


def test_matmul():
    a = Iter(range(3))
    b = Iter(range(4))

    return a @ b == 1 ** 2 + 2 ** 2 + 3 ** 2


def test_find(char_iter):
    assert char_iter.find(lambda c: c == 'l').unwrap() == 'l'


def test_position(char_iter):
    assert char_iter.position(lambda c: c == 'l').unwrap() == 2


def test_find_position(char_iter):
    assert char_iter.find_position(lambda c: c == 'l').unwrap() == (2, 'l')


def test_find_with_no_match(char_iter):
    assert char_iter.find(lambda c: c == 'z').is_nun()


def test_position_with_no_match(char_iter):
    assert char_iter.position(lambda c: c == 'z').is_nun()


def test_find_position_with_no_match(char_iter):
    assert char_iter.find_position(lambda c: c == 'z').is_nun()


def test_collect(int_iter):
    assert int_iter.collect(tuple) == (0, 1, 2, 3, 4)


def test_join(char_iter):
    assert char_iter.join('-') == 'H-e-l-l-o- -w-o-r-l-d-!'


def test_sorted(char_iter):
    assert char_iter.sorted().join() == ''.join(sorted(HELLO_WORLD))


def test_sorted_with_reversed(char_iter):
    assert char_iter.sorted(reversed = True).join() == ''.join(sorted(HELLO_WORLD, reverse = True))
