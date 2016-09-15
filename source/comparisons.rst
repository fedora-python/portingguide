Comparing and Sorting
---------------------

Comparing and sorting undergo a large number of changes in Python 3 but you
can use a lot of functionality described below since Python 2.4.

In short, the ``__cmp__()`` special method is never called, there is no ``cmp``
parameter to any of the sorting-related functions, and there is no builtin
``cmp()`` function.


The ``cmp`` Argument
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: *None*
* Prevalence: Common

In Python 2, there is ``cmp`` agrument in ``.sort()`` or ``sorted()`` functions
which influence order in sorting process. ``cmp`` argument contains function
that returns -1, 0 or 1 when comparing objects. For example::

    >>> def compare(a, b):
    ...     """ Compare objects from last letter to first"""
    ...     return cmp(a[::-1], b[::-1])
    >>> animals = ['dog', 'cat', 'horse', 'cow']
    >>> sorted(animals, cmp=compare)
    ['horse', 'dog', 'cat', 'cow']

In Python 3, ``cmp`` is gone. Instead ``cmp`` there is a ``key`` parameter
which contains a function that returs the key under which to sort.

The difference is then mainly in fact that instead of function that compares
two values directly there is a function that simply returns one value which
will then be compared. Same example implemented in new way with ``key``
parameter::

    >>> def keyfunction(item):
    ...     """Key for comparison that returns reversed string"""
    ...     return item[::-1]
    >>> animals = ['dog', 'cat', 'horse', 'cow']
    >>> sorted(animals, key=keyfunction)
    ['horse', 'dog', 'cat', 'cow']

Using ``key`` parameter is easier and faster because in case of ``cmp``
function for comparison needs to be called multiple times for one item
in set while ``key`` function is called only once for each item in set.

Another advantage of the functions returning key is that it can be easily
used as lambda. Again the same example as before::

    >>> animals = ['dog', 'cat', 'horse', 'cow']
    >>> sorted(animals, key=lambda item: item[::-1])
    ['horse', 'dog', 'cat', 'cow']


The ``cmp`` Function
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: *None*
* Prevalence: Common

Since having ``__cmp__()`` and rich comparison methods goes against the
principle of there is only one obvious way to do something, Python 3
ignores the ``__cmp__()`` method. Also, the cmp() function is gone.

If you really need the ``cmp()`` functionality, you could use the expression::

    (a > b) - (a < b)

as the equivalent for cmp(a, b), but rich comparisons gives you a good way
to handle this changes.

Rich Comparisons
~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: *None*
* Prevalence: Common

Suppose that you have a class to represent person with ``__cmp__()``
implemented::

    class Person(object):
        def __init__(self, firstname, lastname):
             self.first = firstname
             self.last = lastname

        def __cmp__(self, other):
            return cmp((self.last, self.first), (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)

If only thing you need to support is sorting, you just need to change
``__cmp__()`` implementation to ``__lt__()``. The previous example will
look like this::

    class Person(object):
        def __init__(self, firstname, lastname):
             self.first = firstname
             self.last = lastname

        def __lt__(self, other):
            return ((self.last, self.first) < (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)

Since Python 3.2 there is a simple way how to support other comparison
operators without separated implementation for each of them. Solution is
``@total_ordering`` decorator from ``functools`` module.

If you want to use ``@total_ordering`` decorator, your class only has to
implement one of ``__lt__()``, ``__le__()``, ``__gt__()``, or ``__ge__()``
and in addition it should implement ``__eq__()``. If these conditions are
satisfied, you can use ``@total_ordering`` to gain the rest of comparison
operators in your class.

Final implementation might look like this::

    from functools import total_ordering

    @total_ordering
    class Person(object):

        def __init__(self, firstname, lastname):
            self.first = firstname
            self.last = lastname

        def __eq__(self, other):
            return ((self.last, self.first) == (other.last, other.first))

        def __lt__(self, other):
            return ((self.last, self.first) < (other.last, other.first))

        def __repr__(self):
            return "%s %s" % (self.first, self.last)

But sometimes it might be better to implement all six comparison methods
manually because easy solution with ``@total_ordering`` does come at
the cost of slower execution and more complex stack traces for the
derived comparison methods.
