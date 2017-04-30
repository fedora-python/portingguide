Built-In Function Changes
-------------------------

Python 3 saw some changes to built-in functions.
These changes are detailed in this section.


.. _print-function:

The ``print()`` function
~~~~~~~~~~~~~~~~~~~~~~~~

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


Safe ``input()``
~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_input_six``
* Prevalence: Uncommon

In Python 2, the function :func:`py2:input` read a line from standard input,
*evaluated it as Python code*, and returned the result.
This is almost never useful – most users aren't expected to know Python syntax.
It is also a security risk, as it allows users to run arbitrary code.

Python 2 also had a sane version, :func:`py2:raw_input`, which read a line and
returned it as a string.

In Python 3, :func:`py3:input` has the sane semantics, and ``raw_input`` was
removed.

The :ref:`six` library includes a helper, ``six.moves.input``, that has the
Python 3 semantics in both versions.

The recommended fixer will import that helper as ``input``, replace
``raw_input(...)`` with ``input(...)``, and replace ``input(...)`` with
``eval(input(...))``.
After running it, examine the output to determine if any :func:`eval`
it produces is really necessary.


.. _file-builtin:

Removed ``file()``
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_file`` (but see below)
* Prevalence: Rare

In Python 2, :func:`file` was the type of an open file. It was used in two
ways:

* To open files, i.e. as an alias for :func:`open`. The documentation mentions
  that ``open`` is more appropriate for this case.
* To check if an object is a file, as in ``isinstance(f, file)``.

The recommended fixer addresses the first use: it will rewrite all calls to
``file()`` to ``open()``.
If your code uses the name ``file`` for a different function, you will need
to revert the fixer's change.

The fixer does not address the second case. There are many kinds of file-like
objects in Python; in most circumstances it is better to check for
a ``read`` or ``write`` method instead of querying the type.
This guide's :ref:`section on strings <str-file-io>` even recommends using
the ``io`` library, whose ``open`` function produces file-like objects that
aren't of the ``file`` type.

If type-checking for files is necessary, we recommend using a tuple of types
that includes :class:`io.IOBase` and, under Python 2, ``file``::

    import six
    import io

    if six.PY2:
        file_types = file, io.IOBase
    else:
        file_types = (io.IOBase,)

    ...
    isinstance(f, file_types)


Removed ``apply()``
~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_apply`` (but see below)
* Prevalence: Common

In Python 2, the function :func:`apply` was built in.
It was useful before Python added support for passing an argument list
to a function via the ``*`` syntax.

The code::

    arguments = [7, 3]
    apply(complex, arguments)

can be replaced with::

    arguments = [7, 3]
    complex(*arguments)

The recommended fixer replaces all calls to ``apply`` with the new syntax.
If the variable ``apply`` names a different function
in some of your modules, revert the fixer's changes in that module.


Moved ``reduce()``
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_reduce``
* Prevalence: Uncommon

In Python 2, the function :func:`reduce` was built in.
In Python 3, in an effort to reduce the number of builtins, it was moved
to the :mod:`functools` module.

The new location is also available in Python 2.6+, so this removal can be fixed
by importing it for all versions of Python::

    from functools import reduce

The recommended fixer will add this import automatically.


.. _exec:

The ``exec()`` function
~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_exec``
* Prevalence: Rare

In Python 2, :func:`exec` was a statement. In Python 3, it is a function.

There were three cases for the statement form of ``exec``::

    exec some_code
    exec some_code in globals
    exec some_code in globals, locals

Similarly, the function ``exec`` takes one to three arguments::

    exec(some_code)
    exec(some_code, globals)
    exec(some_code, globals, locals)

In Python 2, the syntax was extended so the first expression may be
a 2- or 3-tuple. This means the function-like syntax works even in Python 2.

The recommended fixer will convert all uses of ``exec`` to the function-like
syntax.


Removed ``execfile()``
~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None recommended
* Prevalence: Very rare

Python 2 included the function :func:`py2:execfile`, which executed
a Python file by name.
The call::

    execfile(filename)

was equivalent to::

    def compile_file(filename):
        with open(filename) as f:
            return compile(f.read(), filename, 'exec')

    exec(compile_file(filename))

If your code uses ``execfile``, add the above ``compile_file`` function to
an appropriate place, then change all calls to ``execfile`` to ``exec``
as above.

Although :ref:`python-modernize` has an ``execfile`` fixer, we don't recommend
using it, as it doesn't close the file correctly.

.. XXX: file an issue in python-modernize


Moved ``reload()``
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Very rare

The :func:`~importlib.reload` function was built-in in Python 2.
In Python 3, it is moved to the ``importlib`` module.

Python 2.7 included an ``importlib`` module, but without a ``reload`` function.
Python 2.6 and below didn't have an ``importlib`` module.

If your code uses ``reload()``, import it conditionally on Python 3::

    import six

    if not six.PY2:
        from importlib import reload



Moved ``intern()``
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Very rare

The :func:`~sys.intern` function was built-in in Python 2.
In Python 3, it is moved to the ``sys`` module.

If your code uses ``intern()``, import it conditionally on Python 3::

    import six

    if not six.PY2:
        from sys import intern


Removed ``coerce()``
~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

Python 3 removes the deprecated function :func:`py2:coerce`, which was only
useful in early versions of Python.

If your code uses it, modify the code to not require it.

If any of your classes defines the special method ``__coerce__``,
remove that as well, and test that the removal did not break semantics.

.. XXX: I've never seen serious use of ``coerce``, so the advice is limited.
