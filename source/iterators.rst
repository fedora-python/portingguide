Iterators
---------

Python 3 brings some changes in return values of well-known functions from
the list to the iterator. The main reason for this change is that iterators
might have less memory consumption than lists in some cases.

If you really need to use lists as result of functions ``map()``,
``filter()``, ``range()`` or ``zip()``, you can use simple fix and
cover its call with ``list()`` function which changes function result
from the iterator to the list.


``map()``, ``filter()``
~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_map -f libmodernize.fixes.fix_filter``
* Prevalence: Common

When mentioned fixer detects call of ``map()`` or ``filter()`` it adds imports
``from six.moves import filter`` or ``from six.moves import map`` to the top
of the file. In Python 3, these imports don't make any change, but in Python 2
they import functions ``ifilter()`` or ``imap()`` from ``itertools`` module
under the original names.

The mentioned command is able to do a good service in many cases and discerns
use of functions ``map()`` and ``filter()`` and thus decide whether the change
of returned value is necessary.

But nothing is perfect and therefore always pay attention to the outcome.
In some cases, the use of ``list()`` is completely unnecessary and is
a better to redesign a code.

Let's walk through two examples of fixer behavior. If anonymous function
``lambda:`` is used in the function call of ``map()`` or ``filter()`` then
fixer will change it to list comprehension. For example::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    powered = map(lambda x: x**2, numbers)

    for number in filter(lambda x: x < 20, powered):
        print(number)

Will be changed to::

    numbers = [1, 2, 3, 4, 5, 6, 7]
    
    powered = [x**2 for x in numbers]

    for number in [x for x in powered if x < 20]:
        print(number)

However, if you use named function as an argument, fixer decides when
is necessary to change it to list (variable assignment) and when is possible
to leave it as an iterator. For example::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    def power_function(x):
        return(x**2)

    def filter_function(x):
        return x < 20

    powered = map(power_function, numbers)

    for number in filter(filter_function, powered):
        print(number)

Will be changed to::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    def power_function(x):
        return(x**2)

    def filter_function(x):
        return x < 20

    powered = list(map(power_function, numbers))

    for number in filter(filter_function, powered):
        print(number)


``zip()``
~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_zip``
* Prevalence: Common

The situation with the function ``zip()`` is easier. Fixer again imports
replacement ``from six.moves import zip`` which in Python 2 replaces
the function ``zip()`` with the function ``izip()`` from the ``itertools``
module and then it wraps the function call ``zip()`` with function ``list()``
where it seems appropriate.


``range()``
~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_xrange_six``
* Prevalence: Common

Because in Python 2 there are both ``range()`` and ``xrange()`` functions,
the situation here is slightly different.

As in previous cases, fixer imports function ``range()`` from ``six.moves``
module a then use ``list()`` as wrapper where it seems appropriate.
Because it is obvious where we want to implement an iterator
(call ``xrange()``) and where we want a list (call ``range()``) fixer
makes a change from::

    itr = xrange(a)
    lst = range(b)

to::

    itr = range(a)
    lst = list(range(b))


``next()``
~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_next``
* Prevalence: Common

In Python 2 you get the next result from an iterator by calling the iterators
``.next()`` method. In Python 3 there is instead a ``next()`` builtin.

``next()`` builtin is available in Python 2 since version 2.6. If you need to
support older version you can implement this function by yourself or use
``advance_iterator()`` from ``six`` module.
