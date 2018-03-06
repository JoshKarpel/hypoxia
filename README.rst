Hypoxia
=======

As we all know, Python is a multi-paradigm language.
We can write simple scripts, complex object-oriented applications, mostly-functional programs, and many other styles, all under the same umbrella.
There are even ambitious projects like `Coconut <http://coconut-lang.org/>`_, which define a superset of Python that gives you different idioms to work with.

But what if you don't want to work with something that **expands** Python?
What if you just want to replace `beautiful, idiomatic Python code <https://youtu.be/OSGv2VnC0go>`_ with beautiful, idiomatic Rust code?

Welcome to Hypoxia:

::

    from hypoxia import HashMap

    h = HashMap(foo = 'bar')

    assert h['foo'].unwrap() == 'bar'
    assert h['kazoo'].unwrap_or('vuvuzela') == 'vuvuzela'

    h['num'] = 2

    assert h['num'].map(lambda x: x ** 2).unwrap_or(0) == 4
    assert h['notnum'].map(lambda x: x ** 2).unwrap_or(0) == 0

Never again will we have to write the horrifically confusing

::

    d = dict(num = 2)
    assert d.get('num', 0) ** 2 == 4
    assert d.get('notnum', 0) ** 2 == 0

Read some configuration values from a file, or use defaults if something goes wrong:

::

    from hypoxia import open_file

    config = open_file('.config, mode = 'r').map(parse_config).unwrap_or(DEFAULT_CONFIG)

You might be thinking: hold on, you didn't read that file using `open` in a `with` block, so how do you know if it was closed correctly?
Well, in Rust, this is never a problem because the cleanup happens when the file reference leaves scope.
So we'll just assume that Python is doing the right thing here.

Why?
----

It is our sacred duty to rewrite everything in Rust.

But Seriously, Why?
-------------------

Because I was learning Rust and had an idea so bad that I just had to do it.

License
-------

Hypoxia is licensed under the `WTFPL <http://www.wtfpl.net/>`_.
That means you can do whatever the fuck you want with it.
