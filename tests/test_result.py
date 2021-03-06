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


def test_and_with_ok_ok():
    x = Ok(2)
    y = Ok(3)

    assert x.and_(y) == Ok(3)


def test_and_with_ok_err():
    x = Ok(2)
    y = Err(Exception('late'))

    assert x.and_(y) == Err(Exception('late'))


def test_and_with_err_ok():
    x = Err(Exception('early'))
    y = Ok(2)

    assert x.and_(y) == Err(Exception('early'))


def test_and_with_err_err():
    x = Err(Exception('early'))
    y = Err(Exception('late'))

    assert x.and_(y) == Err(Exception('early'))


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


def test_unwrap_with_ok():
    x = Ok(2)

    assert x.unwrap() == 2


def test_unwrap_with_err():
    x = Err(Exception('error message'))

    with pytest.raises(Panic):
        x.unwrap()


def test_unwrap_or_with_ok():
    x = Ok(2)

    assert x.unwrap_or(0) == 2


def test_unwrap_or_with_err():
    x = Err(Exception('error message'))

    assert x.unwrap_or(0) == 0


def test_unwrap_or_else_with_ok():
    x = Ok(2)

    assert x.unwrap_or_else(lambda x: x.args[0].upper()) == 2


def test_unwrap_or_else_with_err():
    x = Err(Exception('error message'))

    assert x.unwrap_or_else(lambda x: x.args[0].upper()) == 'ERROR MESSAGE'


def test_unwrap_err_with_ok():
    x = Ok(2)

    with pytest.raises(Panic):
        x.unwrap_err()


def test_unwrap_err_with_err():
    x = Err(Exception('error message'))

    assert x.unwrap_err().args == Exception('error message').args


def test_iter_with_ok():
    x = Ok(2)

    assert list(iter(x)) == [2]


def test_iter_with_err():
    x = Err(Exception('error message'))

    assert list(iter(x)) == []


def test_hash_ok():
    x = Ok(2)
    y = Ok(2)

    assert x == y
    assert hash(x) == hash(y)


def test_hash_ok_not_eq():
    x = Ok(2)
    y = Ok(3)

    assert x != y
    assert hash(x) != hash(y)


def test_hash_err():
    x = Err(Exception('error message'))
    y = Err(Exception('error message'))

    assert x == y
    assert hash(x) == hash(y)


def test_hash_err_different_type_same_message():
    x = Err(IOError('error message'))
    y = Err(TypeError('error message'))

    assert x != y
    assert hash(x) != hash(y)


def test_hash_err_same_type_different_message():
    x = Err(Exception('foo'))
    y = Err(Exception('bar'))

    assert x != y
    assert hash(x) != hash(y)
