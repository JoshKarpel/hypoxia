from hypoxia import impl


class Foo:
    def method(self):
        print(self.__class__.__name__.upper())


class Baz():
    pass


@impl(Foo, Baz)
def impl_method(self):
    print(self.__class__.__name__.lower())


f = Foo()

print(f.method)
print(f.impl_method)

f.method()
f.impl_method()

print(type(f.method))
print(type(f.impl_method))

b = Baz()
b.impl_method()
