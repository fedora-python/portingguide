Dictionaries
------------

There are two most significant changes related to dictionaries in Python 3.

Removed ``dict.has_key()``
~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.has_key`` (See caveat below)
* Prevalence: Common

The ``dict.has_key()`` method, long deprecated in favor of the ``in`` operator,
is no longer available in Python 3.

Instead of::

    dictionary.has_key('keyname')

you should use::

    'keyname' in dictionary

Note that the recommended fixer replaces all calls to any ``has_key`` method;
it does not check that its object is actually a dictionary.

If you use a third-party non-dict-like class, it should implement ``in``
already.
If not, complain to its author: it should have been added as part of
Python 3 support.

If your own codebase contains a custom dict-like class, add
a :meth:`~py3:object.__contains__` method to it to implement the
``in`` operator.
If possible, mark the ``has_key`` method as deprecated.
Then run the fixer, and review the output.
Typically, the fixer's changes will need to be be reverted in tests for the
``has_key`` method itself.

If you are using objects with unrelated semantics for the attribute
``has_key``, you'll need to review the fixer's output and revert its changes
for such objects.


Randomized Key Order
~~~~~~~~~~~~~~~~~~~~

XXX


Dict Views and Iterators
~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_dict_six`` (See caveat below)
* Prevalence: Common

The methods :meth:`py3:dict.keys`, :meth:`py3:dict.items` and
:meth:`py3:dict.values()` now return views instead of lists.

The following are the most important differences:

* Unlike lists, a view does not hold copy the data. Updates to the underlying
  dict are reflected in the view.
* Key and value views support set operations, such as intersection and union

The following common operations work the same between views and lists, as long
as the underlying dict is not modified:

* Iteration (e.g. ``for x in d.values()``)
* Member testing (e.g. ``if x in d.values()``)
* Length testing (e.g. ``len(d.values())``)

The methods :meth:`py2:dict.iterkeys`, :meth:`py2:dict.iteritems`
and :meth:`py2:dict.itervalues()`, and the less-used :meth:`py2:dict.viewkeys`, :meth:`py2:dict.viewitems()` and :meth:`py2:dict.viewvalues()`,
are no longer available.


Cross-Version Iteration and Views
.................................

To get iterators in both Python 2 and Python 3, calls to ``iterkeys()``,
``itervalues()`` and ``iteritems()`` can be replaced by calls to functions
from the :ref:`six` library::

    six.iterkeys(dictionary)
    six.iteritems(dictionary)
    six.itervalues(dictionary)

Similarly, ``viewkeys()``, ``viewvalues()`` and ``viewitems()`` have
compatibility wrappers in :ref:`six`::

    six.viewkeys(dictionary)
    six.viewitems(dictionary)
    six.viewvalues(dictionary)

In Python 3, both ``iter*`` and ``view*`` functions correspond to ``keys()``,
``items()``, and ``values()``.

However, we recommend avoiding the ``six`` wrappers whenever it's sensible.
For example, one often sees ``iter*`` functions in Python 2 code::

    for v in dictionary.itervalues():
        print(v)

To be compatible with Python 3, this code can be changed to use ``six``::

    for v in six.itervalues(dictionary):
        print(v)

... or a “native” method::

    for v in dictionary.values():
        print(v)

The latter is more readable.
However, it can be argued that the former is more memory-efficient in Python 2,
as a new list is not created.

In most real-world use cases, the memory difference is entirely negligible:
the extra list is a fraction of the size of a dictionary, and tiny compared
to the data itself.
Any speed difference is almost always negligible.
So, we suggest using the more readable variant unless special optimizations
are needed (for example, if the dictionary could contain millions of items
or more).

Fixer caveats
.............

The recommended fixer rewrites the usage of dict methods, but very often
its changes are not ideal.
We recommend treating its output as “markers” that indicate code that needs
to change, but addressing each such place individually by hand.

For example, the fixer will change::

    for key in somedict.keys():
        print key

to::

    for key in list(somedict.keys()):
        print(key)

This change is entirely unnecessary.
The new version is less performant (in  both Python 2 and Python 3),
and less readable.
However, the fixer cannot detect that the loop never changes ``somedict``,
so it emits overly defensive code.

In this case, both speed and readibility can be improved by iterating over
the dict itself::

    for key in somedict:
        print(key)

As another exaple, the fixer will change::

    keys = dictionary.keys()
    keys.sort()

to::

    keys = list(dictionary.keys())
    keys.sort()

but a better solution would be creating a list that is already sorted::

    keys = sorted(dictionary)
