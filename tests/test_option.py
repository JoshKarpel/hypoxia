import pytest

from hypoxia import Some, Nun, Panic, Ok, Err


def test_is_some_with_some():
    x = Some(2)

    assert x.is_some()


def test_is_some_with_nun():
    x = Nun()

    assert not x.is_some()


def test_is_nun_with_some():
    x = Some(2)

    assert not x.is_nun()


def test_is_nun_with_nun():
    x = Nun()

    assert x.is_nun()


def test_unwrap_with_some():
    x = Some(2)

    assert x.unwrap() == 2


def test_unwrap_with_nun():
    x = Nun()

    with pytest.raises(Panic):
        x.unwrap()


def test_unwrap_or_with_some():
    x = Some(2)

    assert x.unwrap_or(0) == 2


def test_unwrap_or_with_nun():
    x = Nun()

    assert x.unwrap_or(0) == 0


def test_unwrap_or_else_with_some(mocker):
    x = Some(2)
    func = mocker.MagicMock(return_value = 0)

    assert x.unwrap_or_else(func) == 2
    assert func.call_count == 0


def test_unwrap_or_else_with_nun(mocker):
    x = Nun()
    func = mocker.MagicMock(return_value = 0)

    assert x.unwrap_or_else(func) == 0
    assert func.call_count == 1


def test_map_with_some():
    x = Some(2)

    assert x.map(lambda y: y ** 2) == Some(4)


def test_map_with_nun():
    x = Nun()

    assert x.map(lambda y: y ** 2) == Nun()


def test_map_or_with_some():
    x = Some(2)

    assert x.map_or(lambda y: y ** 2, 0) == 4


def test_map_or_with_nun():
    x = Nun()

    assert x.map_or(lambda y: y ** 2, 0) == 0


def test_map_or_else_with_some():
    x = Some(2)

    assert x.map_or_else(lambda y: y ** 2, lambda: 0) == 4


def test_map_or_else_with_nun():
    x = Nun()

    assert x.map_or_else(lambda y: y ** 2, lambda: 0) == 0


def test_ok_or_with_some():
    x = Some(2)

    assert x.ok_or(Exception('error message')) == Ok(2)


def test_ok_or_with_nun():
    x = Nun()

    assert x.ok_or(Exception('error message')) == Err(Exception('error message'))


def test_ok_or_else_with_some():
    x = Some(2)

    assert x.ok_or_else(lambda: Exception('error message')) == Ok(2)


def test_ok_or_else_with_nun():
    x = Nun()

    assert x.ok_or_else(lambda: Exception('error message')) == Err(Exception('error message'))


def test_iter_with_some():
    x = Some(2)

    assert list(iter(x)) == [2]


def test_iter_with_nun():
    x = Nun()

    assert list(iter(x)) == []


def test_and_with_some_some():
    x = Some(2)
    y = Some(3)

    assert x.and_(y) == Some(3)


def test_and_with_some_nun():
    x = Some(2)
    y = Nun()

    assert x.and_(y) == Nun()


def test_and_with_nun_some():
    x = Nun()
    y = Some(2)

    assert x.and_(y) == Nun()


def test_and_with_nun_nun():
    x = Nun()
    y = Nun()

    assert x.and_(y) == Nun()


def test_and_then_with_some():
    x = Some(2)

    assert x.and_then(lambda y: y ** 2) == Some(4)


def test_and_then_with_nun():
    x = Nun()

    assert x.and_then(lambda y: y ** 2) == Nun()


def test_or_with_some_some():
    x = Some(2)
    y = Some(3)

    assert x.or_(y) == Some(2)


def test_or_with_some_nun():
    x = Some(2)
    y = Nun()

    assert x.or_(y) == Some(2)


def test_or_with_nun_some():
    x = Nun()
    y = Some(2)

    assert x.or_(y) == Some(2)


def test_or_with_nun_nun():
    x = Nun()
    y = Nun()

    assert x.or_(y) == Nun()


def test_or_else_with_some():
    x = Some(2)

    assert x.or_else(lambda: 5) == Some(2)


def test_or_else_with_nun():
    x = Nun()

    assert x.or_else(lambda: 5) == Some(5)


def test_get_or_insert_with_some():
    x = Some(2)

    assert x.get_or_insert(5) == 2


def test_get_or_insert_with_nun():
    x = Nun()

    assert x.get_or_insert(5) == 5
    assert isinstance(x, Some)


def test_get_or_insert_with_with_some():
    x = Some(2)

    assert x.get_or_insert_with(lambda: 5) == 2


def test_get_or_insert_with_with_nun():
    x = Nun()

    assert x.get_or_insert_with(lambda: 5) == 5
    assert isinstance(x, Some)


def test_hash_some():
    x = Some(2)
    y = Some(2)

    assert x == y
    assert hash(x) == hash(y)


def test_hash_some_not_eq():
    x = Some(2)
    y = Some(3)

    assert x != y
    assert hash(x) != hash(y)


def test_hash_nun():
    x = Nun()
    y = Nun()

    assert x == y
    assert hash(x) == hash(y)
