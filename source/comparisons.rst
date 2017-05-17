Comparing and Sorting
---------------------

Python 3 is strict when comparing objects of disparate types. It also drops
*cmp*-based comparison and sorting in favor of rich comparisons
and key-based sorting, modern alternatives that have been available at least
since Python 2.4.
Details and porting strategies follow.


.. index:: sort, comparison
.. index:: TypeError; comparison
.. index:: TypeError; sort

Unorderable Types
~~~~~~~~~~~~~~~~~

The strict approach to comparing in Python 3 makes it generally impossible to
compare different types of objects.

For example, in Python 2, comparing ``int`` and ``str`` works
(with results that are unpredictable across Python implementations)::

    >>> 2 < '2'
    True

but in Python 3, it fails with a well described error message::

    >>> 2 < '2'
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: unorderable types: int() < str()

The change usually manifests itself in sorting lists: in Python 3, lists
with items of different types are generally not sortable.

If you need to sort heterogeneous lists, or compare different types of objects,
implement a key function to fully describe how disparate types
should be ordered.


.. index:: __eq__, __ne__, __lt__, __le__, __gt__, __ge__, __cmp__
.. index:: TypeError; __cmp__

Rich Comparisons
~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Common

The :meth:`~py2:object.__cmp__` special method is no longer honored in Python 3.

In Python 2, ``__cmp__(self, other)`` implemented comparison between two
objects, returning a negative value if ``self < other``, positive if
``self > other``, and zero if they were equal.

This approach of representing comparison results is common in C-style
languages. But, early in Python 2 development, it became apparent that
only allowing three cases for the relative order of objects is too limiting.

This led to the introduction of *rich comparison* methods, which assign a
special method to each operator:

    ======== ============
    Operator Method
    ======== ============
     ==      ``__eq__``
     !=      ``__ne__``
     <       ``__lt__``
     <=      ``__le__``
     >       ``__gt__``
     >=      ``__ge__``
    ======== ============

Each takes the same two arguments as *cmp*, and must return either a result
value (typically Boolean), raise an exception, or return ``NotImplemented``
to signal the operation is not defined.

In Python 3, the *cmp* style of comparisons was dropped.
All objects that implemented ``__cmp__`` must be updated to implement *all* of
the rich methods instead.
(There is one exception: on Python 3, ``__ne__`` will, by default, delegate to
``__eq__`` and return the inverted result . However, this is *not* the case
in Python 2.)

To avoid the hassle of providing all six functions, you can implement
``__eq__``, ``__ne__``, and only one of the ordering operators, and use the
:func:`functools.total_ordering` decorator to fill in the rest.
Note that the decorator is not available in Python 2.6. If you need
to support that version, you'll need to supply all six methods.

The ``@total_ordering`` decorator does come with the cost of somewhat slower
execution and more complex stack traces for the derived comparison methods,
so defining all six explicitly may be necessary in some cases even if
Python 2.6 support is dropped.

As an example, suppose that you have a class to represent a person with
``__cmp__()`` implemented::

    class Person(object):
        def __init__(self, firstname, lastname):
             self.first = firstname
             self.last = lastname

        def __cmp__(self, other):
            return cmp((self.last, self.first), (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)

With ``total_ordering``, the class would become::

    from functools import total_ordering

    @total_ordering
    class Person(object):

        def __init__(self, firstname, lastname):
            self.first = firstname
            self.last = lastname

        def __eq__(self, other):
            return ((self.last, self.first) == (other.last, other.first))

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return ((self.last, self.first) < (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)

If ``total_ordering`` cannot be used, or if efficiency is important,
all methods can be given explicitly::

    class Person(object):

        def __init__(self, firstname, lastname):
            self.first = firstname
            self.last = lastname

        def __eq__(self, other):
            return ((self.last, self.first) == (other.last, other.first))

        def __ne__(self, other):
            return ((self.last, self.first) != (other.last, other.first))

        def __lt__(self, other):
            return ((self.last, self.first) < (other.last, other.first))

        def __le__(self, other):
            return ((self.last, self.first) <= (other.last, other.first))

        def __gt__(self, other):
            return ((self.last, self.first) > (other.last, other.first))

        def __ge__(self, other):
            return ((self.last, self.first) >= (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)


.. index:: cmp; removed built-in function
.. index:: NameError; cmp

The ``cmp`` Function
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Common

As part of the move away from *cmp*-style comparisons, the :func:`py2:cmp`
function was removed in Python 3.

If it is necessary (usually to conform to an external API), you can provide it
with this code::

    def cmp(x, y):
        """
        Replacement for built-in funciton cmp that was removed in Python 3

        Compare the two objects x and y and return an integer according to
        the outcome. The return value is negative if x < y, zero if x == y
        and strictly positive if x > y.
        """

        return (x > y) - (x < y)

The expression used is not straightforward, so if you need the functionality,
we recommend adding the full, documented function to your project's utility
library.


.. index:: cmp; argument of sort()
.. index:: TypeError; key function

The ``cmp`` Argument
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Uncommon

In Python 2, ``.sort()`` or ``sorted()`` functions have a ``cmp`` parameter,
which determines the sort order. The argument for ``cmp`` is a function
that, like all *cmp*-style functions, returns a negative, zero, or positive
result depending on the order of its two arguments.

For example, given a list of instances of a Person class (defined above)::

    >>> actors = [Person('Eric', 'Idle'),
    ...           Person('John', 'Cleese'),
    ...           Person('Michael', 'Palin'),
    ...           Person('Terry', 'Gilliam'),
    ...           Person('Terry', 'Jones')]
    ...

one way to sort it by last name in Python 2 would be::

    >>> def cmp_last_name(a, b):
    ...     """ Compare names by last name"""
    ...     return cmp(a.last, b.last)
    ...
    >>> sorted(actors, cmp=cmp_last_name)
    ['John Cleese', 'Terry Gilliam', 'Eric Idle', 'Terry Jones', 'Michael Palin']

This function is called many times – O(*n* log *n*) – during the comparison.

As an alternative to *cmp*, sorting functions can take a keyword-only ``key``
parameter, a function that returns the key under which to sort::

    >>> def keyfunction(item):
    ...     """Key for comparison by last name"""
    ...     return item.last
    ...
    >>> sorted(actors, key=keyfunction)
    ['John Cleese', 'Terry Gilliam', 'Eric Idle', 'Terry Jones', 'Michael Palin']

The advantage of this approach is that this function is called only once for
each item.
When simple types such as tuples, strings, and numbers are used for keys,
the many comparisons are then handled by optimized C code.
Also, in most cases key functions are more readable than *cmp*: usually,
people think of sorting by some aspect of an object (such as last name),
rather than by comparing individual objects.
The main disadvantage is that the old *cmp* style is commonly used in
C-language APIs, so external libraries are likely to provide similar functions.

In Python 3, the ``cmp`` parameter was removed, and only ``key`` (or no
argument at all) can be used.

There is no fixer for this change.
However, discovering it is straightforward: the calling ``sort`` with the
``cmp`` argument raises TypeError in Python 3.
Each *cmp* function must be replaced by a *key* function.
There are two ways to do this:

* If the function did a common operation on both arguments, and then compared
  the results, replace it by just the common operation.
  In other words, ``cmp(f(a), f(b))`` should be replaced with ``f(item)``
* If the above does not apply, wrap the *cmp*-style function with
  :func:`functools.cmp_to_key`. See its documentation for details.

  The ``cmp_to_key`` function is not available in Python 2.6, so if you need
  to support that version, you'll need copy it `from Python sources`_

.. _from Python sources: https://hg.python.org/cpython/file/2.7/Lib/functools.py
