Numbers
-------

There have been two major changes in how Python 3 handles numbers:
true division replaces truncating division, and the ``long``
type was merged into ``int``.

This section describes these changes in detail, along with other, minor ones.


.. index:: division
.. index:: TypeError; division

Division
~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Future import: ``from __future__ import division``
* Prevalence: Common

.. todo:: Link future import

In Python 2, dividing two integers resulted in an integer::

    >>> print 2 / 5
    0

This *truncating division* was inherited from C-based languages,
but confused people who don't know those languages,
such as those coming from Javascript or pure math.

In Python 3, dividing two integers results in a float::

    >>> print(2 / 5)
    0.4

The ``//`` operator, which was added all the way back in Python 2.2,
always performs truncating division::

    while_minutes = seconds // 60

The ``from __future__ import division`` directive causes the ``/`` operator
to behave the same in Python 2 as it does in Python 3.
We recommend adding it to all modules that use the division operator,
so that differences between Python versions are minimal.

When adding the future import, check all divisions in the file and decide
if the operator should be changed to ``//``.


.. index:: __div__, __floordiv__, __truediv__

Special Methods
...............

To overload the ``/`` operator for a class in Python 2, one defined
the ``__div__`` special method.
With the division change, there are two methods to define:


* ``__floordiv__``

    Defines the behavior of the ``//`` operator.

* ``__truediv__``

    Defines the behavior of the ``/`` operator in Python 3, and
    in Python 2 when the ``division`` future import is in effect.

* ``__div__``

    Defines the behavior of the ``/`` operator in Python 2, when
    the ``division`` future import is *not* in effect.

    Not used at all in Python 3.

Check all classes that define ``__div__``, and add ``__floordiv__`` and/or
``__truediv__`` as needed.
This can be done with a simple alias::

    class CustomClass(object):
        def __div__(self, other):
            return _divide(self, other)

        __truediv__ = __div__


.. index:: TypeError; int & long

Unification of ``int`` and ``long``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3 does not have a ``long`` type.
Instead, ``int`` itself allows large values (limited only by available memory);
in effect, Python 2's ``long`` was renamed to ``int``.

This change has several consequences.

Removal of the ``long`` type
............................

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_long``
* Prevalence: Common

The ``long`` builtin no longer exists.

In Python 2,  calling ``int`` on a number that doesn't fit in the machine
``int`` range would automatically create a ``long`` with the appropriate value.

The same automatic conversion to ``long`` happened on all operations on ``int``
that overflow: for example, ``10**50`` resulted in a ``long`` on most systems.

The range of Python 2's ``int`` was system-dependent.
Together with the automatic conversion, this means that code that depends
on the ``long``/``int`` distinction is fragile – Python 2 didn't provide
very strong guarantees regarding the distinction.

If your code relies on the distinction, you will need to modify it.

Once your code does not rely on the ``long``/``int`` distinction,
you can replace all calls to ``long`` with ``int``.
The recommended fixer will do this.


.. index:: SyntaxError; L suffix on numbers

.. _long-literals:

The ``L`` suffix not allowed in numeric literals
................................................

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_numliterals`` (but see below)
* Prevalence: Very common

In Python 2, ``12345L`` designated a ``long`` literal.
For numbers that exceed the range of ``int``, the ``L`` suffix was optional:
``1234567890123456789012345678901234567890`` always named a ``long`` on current
architectures.

In Python 3, the ``L`` suffix is not allowed.

In code that does not depend on the ``int``/``long`` distinction, you can
simply drop the ``L`` suffix.
The recommended fixer will do this, along with
:ref:`octal literal fixes <octal-literals>` described below.

If the specific type is important, you will need to refactor the code so that
it does not rely on the distinction, as discussed above.


The ``L`` suffix dropped from the representation
................................................

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

In Python 2, canonical representations of long integers included the ``L`` suffix.
For example, ``repr(2**64)`` was ``18446744073709551616L`` on most systems.
In Python 3, the suffix does not appear.
Note that this only affected ``repr``, the string representation (given by
``str()`` or ``print()``) had no suffix.

The canonical representations are rarely used, except in doctests.

As discussed previously, relying on the ``int``/``long`` distinction is fragile.
By extension, relying on the output of ``repr`` of long numbers is also fragile.
Call ``str()`` instead of ``repr()`` when the result might be a (long) integer.


.. index:: SyntaxError; octal literals

.. _octal-literals:

Octal Literals
~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_numliterals`` (but see below)
* Prevalence: Uncommon

Python 2's other holdover from C-based languages is the syntax of octal
literals: zero-prefixed numbers are interpreted in base 8.
For example, the value of ``0123`` was ``83``, and ``0987`` caused a rather
unhelpful SyntaxError.
This is surprising to those not familiar with C, and it can lead to
hard-to-spot errors.

Python 2.6 introduced the ``0o`` prefix as an alternative to plain ``0``.
Python 3 drops the ``0`` prefix: integer literals that start with ``0`` are
illegal (except zero itself, and ``0x``/``0o``/``0b`` prefixes).

You will need to change the leading zero in all ``0``-prefixed literals
to ``0o``.
The recommended fixer will do this automatically, along with
:ref:`long literal fixes <long-literals>` described above.
