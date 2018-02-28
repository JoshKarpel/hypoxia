from hypoxia import Ok, Err, Some, Nun


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
