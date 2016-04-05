Numbers
-------

There have been two major changes in how Python 3 handles strings:
true division replaces truncating division, and the ``long``
type was merged into ``int``.

This section describes all changes in detail.


Division
~~~~~~~~

* Fixer: None
* Future import: ``from __future__ import division``
* Prevalence: Common

.. todo:: Link future import

In Python 2, dividing two integers resulted in an integer.
This *truncating division* was inherited from C-based languages,
but confused people who don't know those languages,
such as those coming from Javascript, or new learners who only know math::

    >>> print 2 / 5
    0

In Python 3, dividing two integers results in a float::

    >>> print(2 / 5)
    0.4

The ``//`` operator, which was added all the way back in Python 2.2,
always performs truncating division::

    while_minutes = seconds // 60

The ``from __future__ import division`` directive causes the ``/`` operator
to behave the same in Python 2 as it does in Python 3.
We recommend using it in all code that uses the division operator,
so that differences between Python versions are minimal.

When adding a future import, check all divisions in the file and decide
if the operator should be changed to ``//``.


Special Methods
...............

To overload the ``/`` operator for a class in Python 2, one defined
the ``__div__`` special method.
With the divisoin change, there are two methods to define:


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
However, calling ``int`` on a number that doesn't fit in Python 2's ``int``
range will automatically create a ``long`` with the appropriate value.

The same automatic conversion to long happens on all operations on ``int``
that overflow: for example, ``10**50`` results in a long on most systems.

The range of Python 2's ``int`` is system-dependent.
Together with the automatic conversion, this means that code that depends
on the ``long``/``int`` distinction is fragile – Python 2 doesn't provide
very strong guarantees regarding the distinction.

If your code relies on the distinction, you will need to refactor it.

Once your code does not rely on the ``long``/``int`` distinction,
you can replace all calls to ``long`` with ``int``.
The recommended fixer will do this.


.. _long-literals:

``L`` suffix not allowed in numeric literals
............................................

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_numliterals`` (but see below)
* Prevalence: Very common

In Python 2, ``12345L`` designated a ``long`` literal.
For numbers that exceed the range of ``int``, the ``L`` suffix was optional:
``1234567890123456789012345678901234567890`` names a ``long`` on current
architectures.

In Python 3, the ``L`` suffix is not allowed.

In code that does not depend on the ``int``/``long`` distinction,
you can simply drop the ``L`` suffix.
The recommended fixer will do this, along with
:ref:`octal literal fixes <octal-literals>`.

If the specific type is important, you will need to refactor the code so that
it does not rely on the distinction, as discussed above.


``L`` suffix dropped from the representation
............................................

* Fixer: None
* Prevalence: Rare

In Python 2, canonical representations of long integers include the ``L`` suffix.
For example, ``repr(2**64)`` is ``18446744073709551616L`` on most systems.
In Python 3, the suffix does not appear.
Note that this only affects ``repr``, the string representation (as in
``str()`` and ``print()``) has no suffix.

The canonical representations are rarely used, except in doctests.

As discussed previously, relying on the ``int``/``long`` distinction is fragile.
By extension, relying on the output of ``repr`` of long numbers is also fragile.
Call ``str()`` instead of ``repr()`` when the result might be a (long) integer.



.. _octal-literals:

Octal Literals
~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_numliterals`` (but see below)
* Prevalence: Uncommon

Python 2's other holdover from C-based languages is the syntax of octal
literals: zero-prefixed numbers are interpreted in base 8.
For example, the value of ``0123`` is ``83``, and ``0987`` causes a rather
unhelpful SyntaxError.
This is surprising to those not familiar with C, and it can lead to
hard-to-spot errors.

Python 2.6 introduced the ``0o`` prefix as an alternative to plain ``0``.
Python 3 drops the ``0`` prefix: integer literals that start with ``0`` (except
zero itself) are illegal.

You will need to change the leading zero in all ``0``-prefixed literals
to ``0o``.
The recommended fixer will do this automatically, along with
:ref:`long literal fixes <long-literals>`.
