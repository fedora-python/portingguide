Comprehensions
--------------

XXX

Leaking of the Iteration Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: *None*
* Prevalence: Rare

In Python 2, the iteration variable(s) of list comprehensions were considered
local to the code containing the expression. For example::

    >>> powers = [2**i for i in range(10)]
    >>> print(i)
    9

This did *not* apply apply to generators, or to set/dict comprehensions
(added in Python 2.7).

In Python 3, list expressions have their own scope: they are *functions*,
just defined with a special syntax, and automatically called.
Thus, the iteration variable(s) don't “leak” out::

    >>> powers = [2**i for i in range(10)]
    >>> print(i)
    Traceback (most recent call last):
      File "...", line 1, in <module>
    NameError: name 'i' is not defined

In most cases, effects of the change are easy to find, as running the code
under Python 3 will result in a NameError.
To fix this, either rewrite the code to not use the iteration variable after
a list comprehension, or convert the comprehension to a ``for`` loop::

    powers = []
    for i in for i in range(10):
        powers.append(2**i)

In some cases, the change might silently cause different behavior.
This is when a variable of the same name is set before the comprehension,
or in a surrounding scope. For example::

    i = 'global'
    def foo():
        powers = [2**i for i in range(10)]
        return i

    >>> foo()  # Python 2
    9
    >>> foo()  # Python 3
    'global'

Unfortunately, you will need to find and fix these cases manually.

.. XXX: Detect this automatically!

Comprehensions over Tuples
~~~~~~~~~~~~~~~~~~~~~~~~~~

XXX
