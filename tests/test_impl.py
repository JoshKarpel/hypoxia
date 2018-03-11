import pytest

from hypoxia import impl


def test_impl_binds_correctly():
    class Foo:
        def method(self):
            pass

    @impl(Foo)
    def impl_method(self):
        pass

    assert Foo.impl_method == impl_method

    f = Foo()

    assert type(f.impl_method) == type(f.method)
