from hypoxia import HashMap

h = HashMap(foo = 'bar')

assert h['foo'].unwrap() == 'bar'
assert h['kazoo'].unwrap_or('vuvuzela') == 'vuvuzela'

h['num'] = 2

assert h['num'].map(lambda x: x ** 2).unwrap_or(0) == 4
assert h['notnum'].map(lambda x: x ** 2).unwrap_or(0) == 0

d = dict(num = 2)
assert d.get('num', 0) ** 2 == 4
assert d.get('notnum', 0) ** 2 == 0
