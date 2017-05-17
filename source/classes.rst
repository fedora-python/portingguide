Classes
=======

Python 3 drops support for “old-style” classes, and introduces dedicated syntax
for metaclasses. Read on for details.


.. index:: object; object as base class
.. index:: old-style class
.. index:: new-style class

New-Style Classes
~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Very common

Python 2 had two styles of classes: “old-style” and “new-style”.

Old-style classes were defined without a superclass (or by
deriving from other old-style classes)::

    class OldStyle:
        pass

    class OldStyleChild(OldStyle):
        pass

New-style classes derive from a built-in class – in most cases, ``object``::

    class NewStyle(object):
        pass

    class NewInt(int):
        pass

In Python 3, all classes are new-style: ``object`` is the default superclass.

For code compatible across Python versions, all classes should be defined with
explicit superclasses: add ``(object)`` to all class definitions with
no superclass list.
To find all places to change, you can run the following command over
the codebase::

    grep --perl 'class\s+[a-zA-Z_]+:'

However, you will need to test the result thoroughly.
Old- and new-style classes have slightly differend semantics, described below.


.. index:: MRO, method resolution order

Method resolution
-----------------

From a developer's point of view, the main difference between the two is
method resolution in multiple inheritance chains.
This means that if your code uses multiple inheritance, there can be
differences between which method is used for a particular subclass.

The differences are summarized on `the Python wiki`_, and the new semantics
are explained in a `Howto document`_ from Python 2.3.

.. _the Python wiki: https://wiki.python.org/moin/NewClassVsClassicClass
.. _Howto document: https://www.python.org/download/releases/2.3/mro/


Object model details
--------------------

Another difference is in the behavior of arithmetic operations:
in old-style classes, operators like ``+`` or ``%`` generally coerced both
operands to the same type.
In new-style classes, instead of coercion, several special methods
(e.g. ``__add__``/``__radd__``) may be tried to arrive at the result.

Other differences are in the object model: only new-style classes have
:attr:`~class.__mro__` or :meth:`~class.mro`, and writing to special
attributes like ``__bases__``, ``__name__``, ``__class__`` is restricted or
impossible.


.. index:: metaclasses

Metaclasses
~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_metaclass``
* Prevalence: Rare

For metaclasses, Python 2 uses a specially named class attribute::

    class Foo(Parent):
        __metaclass__ = Meta

In Python 3, metaclasses are more powerful, but the metaclass needs to be known
before the body of the class statement is executed.
For this reason, metaclasses are now specified with a keyword argument::

    class Foo(Parent, metaclass=Meta):
        ...

The new style is not compatible with Python 2 syntax.
However, the :ref:`six` library provides a workaround that works in both
versions – a base class named ``with_metaclass``.
This workaround does a bit of magic to ensure that the result is the same
as if a metaclass was specified normally::

    import six

    class Foo(six.with_metaclass(Meta, Parent)):
        pass

The recommended fixer will import ``six`` and add ``with_metaclass``
quite reliably, but do test that the result still works.

