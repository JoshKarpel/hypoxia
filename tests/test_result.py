import pytest

from hypoxia import Ok, Err, Some, Nun, Panic


def test_err_val_must_be_exception():
    with pytest.raises(Panic):
        Err(0)


def test_is_ok_with_ok():
    x = Ok(-3)
    assert x.is_ok()


def test_is_ok_with_err():
    x = Err(Exception("error message"))
    assert not x.is_ok()


def test_is_err_with_ok():
    x = Ok(-3)
    assert not x.is_err()


def test_is_err_with_err():
    x = Err(Exception("error message"))
    assert x.is_err()


def test_ok_with_ok():
    x = Ok(2)
    assert x.ok() == Some(2)


def test_ok_with_err():
    x = Err(Exception("error message"))
    assert x.ok() == Nun()


def test_err_with_ok():
    x = Ok(2)
    assert x.err() == Nun()


def test_err_with_err():
    x = Err(Exception("error message"))
    assert x.err() == Some("error message")


def test_map_with_ok():
    x = Ok(2)
    assert x.map(lambda x: x ** 2) == Ok(4)


def test_map_with_err():
    x = Err(Exception('error message'))
    assert x.map(lambda x: x ** 2) == x


def test_map_err_with_ok():
    x = Ok(2)
    assert x.map_err(lambda x: type(x)(x.args[0].upper())) == x


def test_map_err_with_err():
    x = Err(Exception('error message'))
    assert x.map_err(lambda x: Err(type(x)(x.args[0].upper()))) == Err(Exception('ERROR MESSAGE'))


def test_and_with_ok():
    x = Ok(2)
    assert x.and_(Ok(True)) == Ok(True)


def test_and_with_err():
    x = Err(Exception('error message'))
    assert x.and_(Ok(True)) == x


def test_and_then_with_ok():
    x = Ok(2)
    assert x.and_then(lambda x: Ok(x ** 2)) == Ok(4)


def test_and_then_with_ok_and_then_err():
    x = Ok(2)
    assert x.and_then(lambda x: Err(Exception(x + 1))) == Err(Exception(3))


def test_and_then_with_err():
    x = Err(Exception('error message'))
    assert x.and_then(lambda x: x + 1) == x


def test_or_with_ok():
    x = Ok(2)
    assert x.or_(Err(Exception('error message'))) == x


def test_or_with_err():
    x = Err(Exception('error message'))
    assert x.or_(Ok(5)) == Ok(5)


def test_or_else_with_ok():
    x = Ok(2)
    assert x.or_else(lambda x: Ok(True)) == x


def test_or_else_with_err():
    x = Err(Exception('error message'))
    assert x.or_else(lambda x: Ok(True)) == Ok(True)
