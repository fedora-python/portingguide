Other Core Object Changes
-------------------------

XXX


Function Attributes
~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_paren`` (but see below)
* Prevalence: Rare

In Python, functions are mutable objects that support custom attributes.
In such cases, special attributes (ones provided or used by the Python
language itself) are prefised and postfixed by double underscores.

Function objects predate this convention: their built-in attributes
were named with the ``func_`` prefix instead.
However, the new “dunder” names were available, as aliases, even in Python 2.

Python 3 removes the old names for these attributes:

=================== ====================
Legacy name         New name
=================== ====================
``func_closure``    ``__closure__``
``func_code``       ``__code__``
``func_defaults``   ``__defaults__``
``func_dict``       ``__dict__``
``func_doc``        ``__doc__``
``func_globals``    ``__globals__``
``func_name``       ``__name__``
=================== ====================

The recommended fixer will replace all of the old attribute names with the
new ones.
However, it does not check that the attribute is retreived from
a function object.
If your code uses the ``func_*`` names for other purposes, you'll need to
revert the fixer's changes.


``__oct__``, ``__hex__``
~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

The ``__oct__`` and ``__hex__`` special methods customized conversion of
custom classes to octal or hexadecimal srting representation, i.e. the behavior
of the :func:`oct` and :func:`hex` built-in functions.

Python 3 adds the :func:`bin` function, which converts to binary.
Instead of introducing a third name like ``__bin__``, all three now just
use the integer representation of an object, as returned by the ``__index__``
method.
The ``__oct__`` and ``__hex__`` methods are no longer used.

To support both Python 2 and 3, all three must be specified::

    def IntLike:
        def __init__(self, number):
            self._number = int(number)

        def __index__(self):
            return self._number

        def __hex__(self):
            return hex(self._number)

        def __oct__(self):
            return oct(self._number)

If your code defines ``__oct__`` or ``__hex__``, add an ``__index__`` method
that returns an appropriate integer.
If your ``__oct__`` or ``__hex__`` did not return an octal/hexadecimal
representation of an integer before, you'll need to change any code that
relied on them.


``__getslice__``, ``__setslice__``, ``__delslice__``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

The special methods ``__getslice__``, ``__setslice__`` and ``__delslice__``,
which were deprecated since Python 2.0, are no longer used in Python 3.
Item access was unified under ``__getitem__``, ``__setitem__`` and
``__delitem__``.

If your code uses them, convert them into equivalent ``__getitem__``,
``__setitem__`` and ``__delitem__``, possibly adding the functionality
to existing methods.

Keep in mind that :class:`slice` objects have a ``step`` attribute
in addition to ``start`` and ``stop``.
If your class does not support all steps, remember to raise an error for
the ones you don't support.

For example, the equivalent of::

    class Slicable(object):
        def __init__(self):
            self.contents = list(range(10))

        def __getslice__(self, start, stop):
            return self.contents[start:stop]

        def __setslice__(self, start, stop, value):
            self.contents[start:stop] = value

        def __delslice__(self, start, stop):
            del self.contents[start:stop]

would be::

    class Slicable(object):
        def __init__(self):
            self.contents = list(range(10))

        def __getitem__(self, item):
            if isinstance(item, slice):
                print(slice.step)
                if item.step not in (1, None):
                    raise ValueError('only step=1 supported')
                return self.contents[item.start:item.stop]
            else:
                raise TypeError('non-slice indexing not supported')

        def __setitem__(self, item, value):
            if isinstance(item, slice):
                if item.step not in (1, None):
                    raise ValueError('only step=1 supported')
                self.contents[item.start:item.stop] = value
            else:
                raise TypeError('non-slice indexing not supported')

        def __delitem__(self, item):
            if isinstance(item, slice):
                if item.step not in (1, None):
                    raise ValueError('only step=1 supported')
                del self.contents[item.start:item.stop]
            else:
                raise TypeError('non-slice indexing not supported')


``__bool__``
~~~~~~~~~~~~

Unbound Methods
~~~~~~~~~~~~~~~
