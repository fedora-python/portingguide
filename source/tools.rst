Tools
=====

Several tools exist to automate as much of the porting as possible,
and to check for common errors.
Here is a survey of tools we recommend.


.. _six:

Compatibility library: ``six``
------------------------------

When porting a large piece of software, it is desirable to support both
Python 2 and Python 3 in the same codebase.
Many projects will need this dual support for a long time,
but even those that can drop Python 2 support as soon as the port is done,
will typically go through a period of adding Python 3 support,
in which the software should continue to work on Python 2.

Benjamin Peterson's ``six`` module makes it practical to write such
version-straddling code by offering compatibility wrappers over
the differences.

For example, the Python 3 syntax for specifying metaclasses is not valid
Python 2, and the Python 2 way does nothing in Python 3,
so ``six`` provides an ``add_metaclass`` decorator for this purpose.
It also provides stable names for standard library modules that were
moved or reorganized in Python 3.

Six is a run-time dependency, albeit a very small one.
If your project is unfriendly to third-party dependencies, push for this
one as hard as possible.
If you do not use ``six``, you will most likely end up reimplementing it
or outright copying relevant pieces of it into your code.


.. _python-modernize:

Automated fixer: ``python-modernize``
-------------------------------------

Some steps of the porting process are quite mechanical, and can be automated.
These are best handled by the ``python-modernize`` tool – a code-to-code
translator that takes a Python 2 codebase and updates it to be compatible
with both Python 2 and 3.

The tool builds on top of ``2to3``, a library that comes with Python. ``2to3``
was once intended as the main porting tool. It turned out inadequate for that
task, but ``python-modernize`` (among others) successfully reuses its general
infrastructure.

Assuming code is in version control, you'll generally want to run
``python-modernize`` with the ``-wn`` flags: ``-w`` flag causes the tool to
actually change the affected files, and ``-n`` suppresses creating backups.

The tool operates by applying individual *fixers* – one for each type of
change needed. You can select individual fixers to run using the ``-f`` option.
We've found that running a single fixer at a time results in changes that
are easier to review and more likely to be accepted, so that is what this
guide will recommend.
The order of fixers matters sometimes. This guide will present them in order,
but if you skip around, you will need to pay a bit more attention.

The tool always needs a directory (or individual files) to operate on; usually
you'll use the current directory (``.``).

Combining all that, the recommended invocation is::

    python-modernize -wnf <fixer-name> .

While ``python-modernize`` is useful, it is not perfect.
Some changes it makes might not make sense at all times, and in many cases.
It is necessary to know *what* and *why* is changed, and to review the result
as closely as if a human wrote it.
This guide will provide the necessary background for each fixer as we
go along.


Compatibility headers and guide for C extensions: ``py3c``
----------------------------------------------------------

Some projects involve extension modules written in C/C++, or embed Python in
a C/C++-based application.
An easy way to find these is to search your codebase for ``PyObject``.
For these, we have two pieces of advice:

*

  Even though this is a conservative guide, we encourage you to try porting
  C extensions away from the Cython C API. For wrappers to external libraries
  we recommend `CFFI`_; for code that needs to be fast there's `Cython`_.

  While this is relatively disruptive, the result will very likely be more
  maintainable and less buggy, as well as more portable to alternative Python
  implementations.

*

  If you decide to keep your C extension, follow a dedicated porting guide
  similar to this one, which also comes with a ``six``-like library for C
  extensions: `py3c`_.


Automated checker: ``pylint --py3k``
------------------------------------

Pylint is a static code analyzer that can catch mistakes such as
initialized variables, unused imports, and duplicated code.
It also has a mode that flags code incompatible with Python 3.

If you are already using Pylint, you can run the tool with the
``--py3k`` option on any code that is already ported. This will prevent
most regressions.

You can also run ``pylint --py3k`` on unported code to get an idea of
what will need to change, though ``python-modernize`` is usually a better
choice here.




.. _cffi: https://cffi.readthedocs.org/en/latest/
.. _Cython: http://cython.org/
.. _py3c: http://py3c.readthedocs.org/en/latest/
