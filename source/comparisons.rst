Comparing and Sorting
---------------------

Comparing and sorting undergo a large number of changes in Python 3 but you
can use a lot of functionality described below since Python 2.4.


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

Rich Comparisons
~~~~~~~~~~~~~~~~

