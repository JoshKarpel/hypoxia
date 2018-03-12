import pytest

from hypoxia import impl


@pytest.fixture(scope = 'function')
def dummy_class():
    class Dummy:
        def method(self):
            pass

    return Dummy


def test_impl_has_method_type(dummy_class):
    @impl(dummy_class)
    def impl_method(self):
        pass

    d = dummy_class()

    assert type(d.impl_method) == type(d.method)


def test_impl_method_name_refers_to_None(dummy_class):
    @impl(dummy_class)
    def impl_method(self):
        pass

    assert impl_method is None


def test_impl_is_called_correctly(dummy_class, mocker):
    mock = mocker.MagicMock()

    @impl(dummy_class)
    def impl_method(self):
        mock()

    d = dummy_class()
    d.impl_method()

    assert mock.call_count == 1
