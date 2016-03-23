Exceptions
----------

XXX

.. _except-syntax:

The new ``except`` syntax
~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_except``
* Prevalence: Very common

In Python 2, the syntax for catching exceptions is
``except ExceptionType:``, or ``except ExceptionType, target:`` when the
exception object is desired.
``ExceptionType`` can be a tuple, as in, for example,
``except (TypeError, ValueError):``.

This could result in hard-to-spot bugs: the command
``except TypeError, ValueError:`` (note lack of parentheses) will only handle
``TypeError``. It will also assign the exception object to the name
``ValueError``, shadowing the built-in.

To fix this, Python 2.6 introduced an alternate syntax:
``except ExceptionType as target:``.
In Python 3, the old syntax is no longer allowed.

You will need to switch to the new syntax.
The recommended fixer works quite reliably.


.. _raise-syntax:

The new ``raise`` syntax
~~~~~~~~~~~~~~~~~~~~~~~~~

Iterating Exceptions
~~~~~~~~~~~~~~~~~~~~

Raising Non-Exceptions
~~~~~~~~~~~~~~~~~~~~~~

The Removed ``StandardError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

