Built-In Function Changes
-------------------------

Python 3 saw some changes to built-in functions.
These changes are detailed in this section.


.. _print-function:

``print()``
~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_print``
* Prevalence: Very Common

Before Python first introduced keyword arguments, and even functions with
variable numbers of arguments, it had the ``print`` statement.
It worked for simple use cases, but grew idiosyncratic syntax for advanced
features like (not) ending lines and output to arbitrary files::

    print 'a + b =',
    print a + b
    print >> sys.stderr, 'Computed the sum'

In Python 3, the statement is gone. Instead, you can use the :func:`print`
*function*, which has clear semantics (but requires an extra pair of
parentheses in the common case)::

    print('a + b =', end=' ')
    print(a + b)
    print('Computed the sum', file=sys.stderr)

The function form of ``print`` is available in Python 2.6+, but to use it,
the statement form must be turned off with a future import::

    from __future__ import print_function

The recommended fixer will add the future import and rewrite all uses
of ``print``.


``input()``
~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_input_six``
* Prevalence: Uncommon

In Python 2, the function :func:`py2:input` read a line from standard output,
*evaluated it as Python code*, and returns the result.
This is almost never useful – most users aren't expected to know Python syntax.
It is also a security risk, as it allows users to run arbitrary code.

Python 2 also had a sane version, :func:`py2:raw_input`, which reads a line and
returns it as a string.

In Python 3, :func:`py3:input` has the sane semantics, and ``raw_input`` was
removed.

The :ref:`six` library includes a helper, ``six.moves.input``, that has the
Python 3 semantics in both versions.

The recommended fixer will import that helper as ``input``, replace
``raw_input(...)`` with ``input(...)``, and replace ``input(...)`` with
``eval(input(...))``.
After running it, examine the output to determine if any :func:`eval`
it produces is really necessary.


``file()``
~~~~~~~~~~

XXX


``apply()``
~~~~~~~~~~~

XXX


``reduce()``
~~~~~~~~~~~~

XXX


``exec()``
~~~~~~~~~~

XXX


``execfile()``
~~~~~~~~~~~~~~

XXX


``reload()``
~~~~~~~~~~~~

XXX


``intern()``
~~~~~~~~~~~~

XXX


``coerce()``
~~~~~~~~~~~~

XXX
