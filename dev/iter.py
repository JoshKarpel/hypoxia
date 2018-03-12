from hypoxia import Iter

x = (c for c in 'hello')

print(x)

h = Iter(x)
print(h)

# y = h.map(lambda c: c.upper())
y = h.filter(lambda c: c != 'l')
print(y)

print(''.join(y))

# x = (c for c in 'hello')
