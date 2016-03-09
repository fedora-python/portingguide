Types
=====

From a developer's point of view, the largest change in Python 3
is that where one would use ``str`` in Python 2,
one needs to explicitly choose between *text* and *bytes*:

*

    *text*: human-readable text represented as a sequence of Unicode
    codepoints. Usually, it does not contain unprintable control characters
    such as NULL.

    This type is available as ``str`` in Python 3, and ``unicode``
    in Python 2.

    In code, we will refer to this type as ``unicode`` – a short, unabmbiguous
    name, although one that is not built-in in Python 3.
    Some projects refer to it as ``six.text_type`` (from the :ref:`six`
    library).

*

    *bytes* – binary serialization format suitable for storing data on
    on disk or sending it over the wire, as a sequence of
    integers between 0 and 255.
    Most data – images, sound, configuration info, or *text* – can be
    serialized (encoded) to bytes and deserialized (decoded) from
    bytes, using an appropriate protocol such as PNG, VAW, JSON
    or UTF-8.

    In both Python 2.6+ and 3, this type is available as ``bytes``.

Ideally, every “stringy” value will explicitly be one of these types.

XXX: What to do before you start porting

Additionally, code that supports both Python 2 and 3 in the same codebase
can use what is conceptually a third type:

*

    The “native string” (``str`` – text in py3, bytes in py2): the type
    Python uses internally for data like variable and attribute names,
    and requires for ``__str__``/``__repr__`` output.

Besides strings, there are some changes to other core types,
but those are generally minor and usually don't require planning before
you start porting.


Type checking
-------------

Large, complex codebases with stable interfaces may benefit from automatic
optional type checking provided by mypy_.

This allows verifying the expected types of arguments, return values, and
variables, using a syntax such as::

    def greeting(name):
        # type: (str) -> str
        return 'Hello ' + name + '!'

Mypy employs the concept of *gradual typing*: not all types can be specified,
and type checking is simply not done in that case.
Type specifications can be added selectively – for example only to stable
interfaces, or to code that uses strings heavily.

This guide will not go into detail on mypy.
If you are interested, see the `mypy homepage <http://www.mypy-lang.org/>`_
and the `Python 2-compatible typing specification syntax <https://www.python.org/dev/peps/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code>`_ (``mypy --py2``).



.. _mypy: http://www.mypy-lang.org/
