Exceptions
----------

Very early Python versions used simple strings to signalize errors.
Later, Python allowed raising arbitrary classes, and added specialized
exception classes to the standard library.
For backwards compatibility reasons, some deprecated practices were still
allowed in Python 2.
This presents confusion to learners of the language, and prevents some
performance optimizations.

Python 3 removes the deprecated practices.
It also further consolidates the exception model.
Exceptions are now instances of dedicated classes, and contain all
information about the error: the type, value and traceback.

This chapter mentions all exception-related changes needed to start
supporting Python 3.


.. _except-syntax:

The new ``except`` syntax
~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_except``
* Prevalence: Very common

In Python 2, the syntax for catching exceptions was
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
The recommended fixer works quite reliably, and it also fixes the
:ref:`iter_exc` problem described below.


.. _raise-syntax:

The new ``raise`` syntax
~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_raise -f libmodernize.fixes.fix_raise_six``
* Prevalence: Common

Python 2's ``raise`` statement was designed at a time when exceptions weren't
classes, and an exception's *type*, *value*, and *traceback* components
were three separate objects::

    raise ValueError, 'invalid input'
    raise ValueError, 'invalid input', some_traceback

In Python 3, one single object includes all information about an exception::

    raise ValueError('invalid input')

    e = ValueError('invalid input')
    e.__traceback__ = some_traceback
    raise e

Python 2.6 allows the first variant. For the second, re-raising an exception,
the :ref:`six` library includes a convenience wrapper that works in both
versions::

    import six
    six.reraise(ValueError, 'invalid input',  some_traceback)

The recommended fixers will do these conversions automatically and quite
reliably, but do verify the resulting changes.


.. _exc_scope:
.. index::
    single: NameError (from caught exception)

Caught Exception “Scope”
~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: *None*
* Prevalence: Rare

As :ref:`discussed previously <raise-syntax>`, in Python 3, all information
about an exception, including the traceback, is contained in the exception
object.
Since the traceback holds references to the values of all local variables,
storing an exception in a local variable usually forms a reference cycle,
keeping all local variables allocated until the next garbage collection pass.

To prevent this issue, to quote from :py3:ref:`Python's documentation <try>`:

    When an exception has been assigned using as target, it is cleared at
    the end of the except clause. This is as if ::

        except E as N:
            foo

    was translated to ::

        except E as N:
            try:
                foo
            finally:
                del N

    This means the exception must be assigned to a different name to be
    able to refer to it after the except clause.

Unfortunately, :ref:`python-modernize` does not provide a fixer for this
change.
This issue results in a loud ``NameError`` when tests are run.
When you see this error, apply the recommended fix – assign a different name
to the exception to use it outside the ``except`` clause.


.. _iter_exc:

Iterating Exceptions
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_except`` (but see caveat below)
* Prevalence: Rare

In Python 2, exceptions were *iterable*, so it was possible to “unpack” the
arguments of an exception as part of the ``except`` statement::

    except RuntimeError as (num, message):

In Python 3, this is no longer true, and the arguments must be accessed through
the ``args`` attribute::

    except RuntimeError as e:
        num, message = e.args

The recommended fixer catches the easy cases of unpacking in ``except``
statements.
If your code iterates through exceptions elsewhere, you need to manually
change it to iterate over ``args`` instead.

Additionally, the fixer does not do a good job on single-line suites such as::

    except RuntimeError as (num, message): pass

Inspect the output and break these into multiple lines manually.

.. todo:: Report bug to python-modernize


Raising Non-Exceptions
~~~~~~~~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Rare

In Python 3, an object used with ``raise`` must be an instance of
:py:class:`BaseException`, while Python 2 also allowed old-style classes.
Similarly, Python 3 bans catching non-exception classes in the ``except``
statement.

.. todo:: Link "old-style classes" to their section

Raising non-Exception classes was obsolete as early as in Python 2.0,
but code that does this can still be found.

Each case needs to be handled manually.
If there is a dedicated class for the exception,
make it inherit from :py:class:`Exception`.
Otherwise, switch to using a dedicated Exception class.


The Removed ``StandardError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_standarderror`` (but see caveat below)
* Prevalence: Rare

The :class:`py2:StandardError` class is removed in Python 3.
It was the base class for built-in exceptions, and it proved to be an
unnecessary link in almost any exception's inheritance chain.

The recommended fixer will replace all uses of ``StandardError`` with
``Exception``.
Review the result to check if this is correct.

Some code might rely on the name of an exception class, or on exceptions not
derived from ``StandardError``, or otherwise handle ``StandardError``
specially. You'll need to handle these casses manually.


Removed ``sys.exc_type``, ``sys.exc_value``, ``sys.exc_traceback``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Rare

These exception-related attributes of the ``sys`` module are not thread-safe,
and were deprecated since Python 1.5.
They have been dropped for Python 3.

The information can be retrieved with a call to :py:func:`~sys.exc_info()`::

    exc_type, exc_value, exc_traceback = sys.exc_info()
