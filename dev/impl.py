from hypoxia import impl


class Foo:
    def __init__(self, attr):
        self.attr = attr

    def method(self):
        print(self.attr.upper())


@impl(Foo)
def impl_method(self):
    print(self.attr.lower())


f = Foo('AAAbbb ')

print(f.method)
print(f.impl_method)

f.method()
f.impl_method()

print(type(f.method))
print(type(f.impl_method))

print(globals())

# print(impl_method.__get__(None, type(None)))
# print(impl_method.__get__(f, type(f)))
# impl_method.__get__(f, type(f))()
