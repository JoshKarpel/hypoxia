Hypoxia
=======

As we all know, Python is a multi-paradigm language.
We can write simple scripts, complex object-oriented applications, mostly-functional programs, and many other styles, all under the same umbrella.
There are even ambitious projects like `Coconut <http://coconut-lang.org/>`_, which defines a superset of Python that gives you functional constructs to work with.

But what if you don't want to work with something that **expands** Python?
What if you just want to **replace** `beautiful, idiomatic Python code <https://youtu.be/OSGv2VnC0go>`_ with beautiful, idiomatic Rust code?

Welcome to Hypoxia:

.. code-block:: python

    from hypoxia import HashMap

    h = HashMap(foo = 'bar')
    assert h['foo'].unwrap() == 'bar'
    assert h['kazoo'].unwrap_or('vuvuzela') == 'vuvuzela'

    h['num'] = 2
    assert h['num'].map(lambda x: x ** 2).unwrap_or(0) == 4
    assert h['notnum'].map(lambda x: x ** 2).unwrap_or(0) == 0


Never again will we have to write horrifically confusing code using ``dict.get``'s second argument!

.. code-block:: python

    d = dict(num = 2)
    assert d.get('num', 0) ** 2 == 4
    assert d.get('notnum', 0) ** 2 == 0


Another example: read some configuration values from a file and parse them, or use a default configuration if something goes wrong:

.. code-block:: python

    from hypoxia import open_file

    config = open_file('.config', mode = 'r').map(parse_config).unwrap_or(DEFAULT_CONFIG)

The same code in Python would like involve some explicit exception catching (probably at least two, one for the file IO and one for the parsing), making it much longer than a single line.
As we know from the `Zen of Python <https://www.python.org/dev/peps/pep-0020/>`_, "flat is better than nested", and I think you'll agree that that this code is remarkably flat.

You might be thinking: hold on, are you sure you closed that file handle?
Well, in Rust this is never a problem because the cleanup happens automatically when the file is dropped.
So we'll just assume that Python is doing the right thing here.
If you're less trusting, you could always use the context manager version:

.. code-block:: python

    from hypoxia import File

    with File('.config', mode = 'r') as f:
        config = f.map(parse_config).unwrap_or(DEFAULT_CONFIG)


Wait, back up, what's going on?
-------------------------------

Rust doesn't have exceptions.
Instead, errors and possibly-not-found values are communicated using enumerated types: ``Result`` and ``Option``, respectively.
Hypoxia provides a Rust-like interface for those ideas in pure Python.

In the above examples, indexing the ``HashMap`` doesn't return the value associated with that key, even if it does exist.
Instead, an ``Option`` is returned.
If the lookup succeeded, it's a ``Some`` with the value inside, and if it didn't, it's a ``Nun`` (i.e., ``None``, but ``None`` is, of course, reserved in Python).

Similarly, opening the file doesn't return a file handle.
It returns a ``Result`` with the file handle inside, or an ``Err`` with an exception inside if the operation failed for some reason.


Why?
----

It is our sacred duty to rewrite everything in Rust.


But seriously, why?
-------------------

Because I was learning Rust and had an idea so bad that I just had to do it.

Please don't actually use this in anything real.


License
-------

Hypoxia is licensed under the `WTFPL <http://www.wtfpl.net/>`_.
That means you can do whatever the fuck you want with it.
