import pytest

from hypoxia import Some, Nun, Panic


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

    assert x.map(lambda x: x ** 2) == Some(4)


def test_map_with_nun():
    x = Nun()

    assert x.map(lambda x: x ** 2) == Nun()
