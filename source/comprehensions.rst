Comprehensions
--------------

List comprehensions, a shrtcut for creating lists, have been in Python
since version 2.0.
Python 2.4 added a similar feature – generator expressions;
then 2.7 (and 3.0) introduced set and dict comprehensions.

All three can be thought as syntactic sugar for defining and calling a
generator function, but since list comprehensions came before generators,
they behaved slightly differently than the other two.
Python 3 removes the differences.


.. index:: NameError; list comprehensions
.. index:: list comprehensions; iteration variable

Leaking of the Iteration Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
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


.. index:: SyntaxError; list comprehensions over tuples
.. index:: list comprehensions; over tuples

Comprehensions over Tuples
~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_paren``
* Prevalence: Rare

Python 2 allowed list comprehensions over bare, non-parenthesized tuples:

    >>> [i for i in 1, 2, 3]
    [1, 2, 3]

In Python 3, this is a syntax error. The tuple must be enclosed in parentheses:

    >>> [i for i in (1, 2, 3)]
    [1, 2, 3]

The recommended fixer will add the parentheses in the vast majority of cases.
It does not deal with nested loops, such as
``[x*y for x in 1, 2 for y in 1, 2]``.
These cases are easily found, since they raise ``SyntaxError`` under Python 3.
If they appear in your code, add the parentheses manually.
