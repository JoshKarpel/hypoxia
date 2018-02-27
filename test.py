import result

h = result.HashMap()

h['foo'] = 'bar'

print(h['foo'].unwrap())
print(h['zoom'].unwrap_or('boo'))

print(h.get('five'))

f = result.open_file('/does/not/exist', mode = 'r')
print(f.unwrap())
