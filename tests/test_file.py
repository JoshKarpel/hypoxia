import pathlib

import pytest

from hypoxia import File


def test_write(tmpdir):
    path = pathlib.Path(tmpdir) / 'test.txt'

    with File(path, mode = 'w') as f:
        f = f.unwrap()
        f.write('hello')

    assert f.closed

    with open(path, mode = 'r') as f_from_open:
        assert f_from_open.read() == 'hello'


def test_read_on_file_that_doesnt_exist(tmpdir):
    path = pathlib.Path(tmpdir) / 'test.txt'

    with File(path, mode = 'r') as f:
        assert f.is_err()
