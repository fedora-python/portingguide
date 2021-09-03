Iterators
---------

Python 3 changes return values of several basic functions from list to
iterator. The main reason for this change is that iterators usually cause
better memory consumption than lists.

If you need to keep Python2-compatible behavior, you can wrap the affected
functions with a call to :func:`py3:list`. However, in most cases it is better
to apply a more specific fix.


.. index:: map, filter

New behavior of ``map()`` and ``filter()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixers <python-modernize>` (See caveat below):

  * ``python-modernize -wnf libmodernize.fixes.fix_map``
  * ``python-modernize -wnf libmodernize.fixes.fix_filter``

* Prevalence: Common

In Python 3, the :func:`py3:map` and :func:`py3:filter` functions return
iterators (``map`` or ``filter`` objects, respectively).
In Python 2, they returned lists.

In Python 2, the iterator behavior is available as :func:`py2:itertools.imap`
and :func:`py2:itertools.ifilter`.

The :ref:`six` library provides the iterator behavior under names common to
both Python versions: ``from six.moves import map`` and
``from six.moves import filter``.


Higher-order functions vs. List Comprehensions
..............................................

The ``map`` and ``filter`` functions are often used with ``lambda`` functions
to change or filter iterables. For example::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    powers_of_two = map(lambda x: 2**x, numbers)

    for number in filter(lambda x: x < 20, powers_of_two):
        print(number)

In these cases, the call can be rewritten using a list comprehension,
making the code faster and more readable::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    powers_of_two = [2**x for x in numbers]

    for number in [x for x in powers_of_two if x < 20]:
        print(number)

If named functions, rather than ``lambda``, are used, we also recommend
rewriting the code to use a list comprehension.
For example, this code::

    def power_function(x):
        return(2**x)

    powered = map(power_function, numbers)

should be changed to::

    def power_function(x):
        return(2**x)

    powered = [power_function(num) for num in numbers]

Alternatively, you can keep the higher-order function call, and wrap the
result in ``list``.
However, many people will find the resulting code less readable::

    def power_function(x):
        return(2**x)

    powered = list(map(power_function, numbers))


Iterators vs. Lists
...................

In cases where the result of ``map`` or ``filter`` is only iterated over,
and only once, it makes sense to use a *generator expression* rather than
a list. For example, this code::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    powers_of_two = map(lambda x: 2**x, numbers)

    for number in filter(lambda x: x < 20, powers_of_two):
        print(number)

can be rewritten as::

    numbers = [1, 2, 3, 4, 5, 6, 7]

    powers_of_two = (2**x for x in numbers)

    for number in (x**2 for x in powers_of_two if x < 20):
        print(number)

This keeps memory requirements to a minimum.
However, the resulting generator object is much less powerful than a list:
it cannot be mutated, indexed or sliced, or iterated more than once.


Fixer Considerations
....................

When the recommended fixers detect calls to ``map()`` or ``filter()``, they add
the imports ``from six.moves import filter`` or ``from six.moves import map``
to the top of the file.

In many cases, the fixers do a good job discerning the different usages of
``map()`` and ``filter()`` and, if necessary, adding a call to ``list()``.
But they are not perfect.
Always review the fixers' result with the above advice in mind.

The fixers do not work properly if the names ``map`` or ``filter``
are rebound to something else than the built-in functions.
If your code does this, you'll need to do appropriate changes manually.


.. index:: zip

New behavior of ``zip()``
~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_zip`` (See caveat below)
* Prevalence: Common

Similarly to ``map`` and ``filter`` above, in Python 3, the :func:`py3:zip`
function returns an iterator (specifically, a ``zip`` object).
In Python 2, it returned a list.

The :ref:`six` library provides the iterator behavior under a name common to
both Python versions, using the ``from six.moves import zip`` statement.

With this import in place, the call ``zip(...)`` can be rewritten to
``list(zip(...))``.
Note, however, that the ``list`` is unnecessary when the result is only
iterated over, and only iterated once, as in ``for items in zip(...)``.

The recommended fixer adds the mentioned import, and changes calls to
``list(zip(...)`` if necessary.
If you review the result, you might find additional places where conversion
to ``list`` is not necessary.

The fixer does not work properly if the name ``zip``
is rebound to something else than the built-in function.
If your code does this, you'll need to do appropriate changes manually.


.. index:: range

New behavior of ``range()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_xrange_six`` (See caveat below)
* Prevalence: Common

In Python 3, the :func:`py3:range` function returns an iterable ``range``
object, like the :func:`py2:xrange` function did in Python 2.
The ``xrange`` function was removed in Python 3.

Note that Python 3's ``range`` object, like ``xrange`` in Python 2,
supports many list-like operations: for example indexing, slicing, length
queries using :func:`py3:len`, or membership testing using ``in``.
Also, unlike ``map``, ``filter`` and ``zip`` objects, the ``range`` object
can be iterated multiple times.

The :ref:`six` library provides the "``xrange``" behavior in
both Python versions, using the ``from six.moves import range`` statement.

Using this import, the calls::

    a_list = range(9)
    a_range_object = xrange(9)

can be replaced with::

    from six.moves import range

    a_list = list(range(9))
    a_range_object = range(9)

The fixer does the change automatically.

Note that in many cases, code will work the same under both versions
with just the built-in ``range`` function.
If the result is not mutated, and the number of elements doesn't exceed
several thousands, the list and the range behave very similarly.
In this case, just change ``xrange`` to ``range``; no import is needed.

If the name ``range`` is rebound to something else than the built-in
function, the fixer will not work properly.
In this case you'll need to do appropriate changes manually.


.. index:: next, __next__

New iteration protocol: ``next()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_next`` (See caveat below)
* Prevalence: Common

In Python 3, the built-in function :func:`py3:next()` is used to get the next
result from an iterator.
It works by calling the :meth:`~py3:iterator.__next__` special method,
similarly to how :func:`py3:len()` calls :meth:`~py3:iterator.__len__`.
In Python 2, iterators had the ``next`` method.

The ``next()`` built-in was backported to Python 2.6+, where it calls the
``next`` method.

When getting items from an iterator, the ``next`` built-in function should be
used instead of the ``next`` method. For example, the code::

    iterator = iter([1, 2, 3])
    one = iterator.next()
    two = iterator.next()
    three = iterator.next()

should be rewritten as::

    iterator = iter([1, 2, 3])
    one = next(iterator)
    two = next(iterator)
    three = next(iterator)

Another change concerns custom iterator classes.
These should provide both methods, ``next`` and ``__next__``.
An easy way to do this is to define ``__next__``, and assign that function
to ``next`` as well::

    class IteratorOfZeroes(object):
        def __next__(self):
            return 0

        next = __next__  # for Python 2

The recommended fixer will only do the first change – rewriting ``next`` calls.
Additionally, it will rewrite calls to *any* method called ``next``, whether
it is used for iterating or not.
If you use a class that uses ``next`` for an unrelated purpose, check the
fixer's output and revert the changes for objects of this class.

The fixer will not add a ``__next__`` method to your classes.
You will need to do this manually.

Generators cannot raise ``StopIteration``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

Since Python 3.7, generators cannot raise ``StopIteration`` directly,
but must stop with ``return`` (or at the end of the function).
This change was done to prevent subtle errors when a ``StopIteration``
exception “leaks” between unrelated generators.

For example, the following generator is considered a programming error,
and in Python 3.7+ it raises ``RuntimeError``::

    def count_to(maximum):
        i = 0
        while True:
            yield i
            i += 1
            if i >= maximum:
                raise StopIteration()

Convert the ``raise StopIteration()`` to ``return``.

If your code uses a helper function that can raise ``StopIteration`` to
end the generator that calls it, you will need to move the returning logic
to the generator itself.
