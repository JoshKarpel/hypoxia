from hypoxia import Dwell

x = (c for c in 'hello')

print(x)

h = Dwell(x)
print(h)

# y = h.map(lambda c: c.upper())
y = h.filter(lambda c: c != 'l')
print(y)

print(''.join(y))

x = (c for c in 'hello')
