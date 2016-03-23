Modernization
=============

Before porting to Python 3, you’ll need to make sure that you’re not using
features deprecated even in Python 2. Also, many of Python 3’s improvements
have been backported to Python 2.6, and using them will make the porting
process easier.
As a first step of the porting process, you will need to start using
the new syntax and features.

After this phase, your code will still work with Python 2 only.


General Process
---------------

We recommend that you submit changes (e.g. pull requests, patches, review requests)
for each type of change individually.
This makes your contributions easier to review, especially for cases where
rudimentary changes are needed across the whole codebase.
Of course, you can split each change into smaller chunks if that would make
review easier.

Many of the steps presented here have a corresponding :ref:`python-modernize`
fixer. For these, the corresponding command line is given.
We expect that your code is version-controlled, so these command lines disable
*python-modernize*'s automatic backup creation.

We recommend running tests after each step, so you can spot problems early.


* Syntax of ``except`` - done


``apply()``
-----------

:ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_apply .``

The built-in function :func:`apply <py2:apply>` was deprecated since
Python 2.3, and it is removed in Python 3.
It was superceded by argument unpacking; i.e.
``apply(func, args, kwargs)`` should be replaced with the more general
``func(*args, **kwargs)``.

Watch out for code that binds the function ``apply`` to a different name
and then uses it; the fixer will not catch these cases.
It is useful to search the code for the word ``apply`` after running the fixer.

You should look out for code that uses the name ``apply`` for a different
function, though the fixer will handle most such cases correctly.

``exec``
--------

:ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_exec .``

Python 2's ``exec`` statement was replaced by a built-in function of the same
name, to these replacements:

    * ``exec code`` to ``exec(code)``
    * ``exec code in local_namespace`` to ``exec(code, local_namespace)``
    * ``exec code in local_ns, global_ns`` to ``exec(code, local_ns, global_ns)``



Python 2.6 and 2.7's ``exec`` statement accepts 2- or 3-tuples, making it
compatible with the new syntax.


``execfile()``
--------------

*(No recommended fixer)*

XXX: Give an execfile() function

The ``execfile`` function was removed in Python 3, as it is only a combination of
low-level calls. Instead of::

    execfile(filename, local_ns, global_ns)

(possibly with ``local_ns`` or ``global_ns`` unspecified), you should write::

    with open(filename) as f:
        exec(compile(f.read(), filename, exec), local_ns, global_ns)

You will need to search your codebase for the word ``execfile``,
and handle each occurence appropriately.
For heavy usage, it is also possible to define a function for ``execfile``.
Such a function is not included in :ref:`six` because heavy usage of
``execfile`` is quite rare.

.. note::

    There is a ``fix_execfile`` fixer included in ``python-modernize``, but as
    of this writing, it will emit code that does not close the file.
    Unclosed files may be harmless under CPython on Unix, but can cause issues
    on other interpreters and systems.
    Python 3.6 (!) and newer issues warnings for unclosed files.


Integer Literals
----------------

:ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_numliterals .``

In Python 3, the ``L`` suffix for long integers is no longer accepted.
For large numbers, it is not needed even in Python 2 (the type of
``12345678901234567890`` is ``long`` on most systems).
For small numbers, if your code should not rely on the distinction between
``int`` vs. ``long``; if it does, you will need to rethink your logic.
In Python 2, when an expression involving ``int`` overflows (at
a system-dependent threshold), the result is generally automatically given
as ``long``. This makes code that relies on the distinction fragile.
And in Python 3, there is only one ``int`` type.

In Python 2, octal integer literals are prefixed with ``0``, such as ``0123``.
This turns out to be quite confusing for people not familiar with C.
To make octal literals more obvious, Python 2.6 introduced the ``0o`` prefix,
similar to ``0x`` for hexadecimal numbers. In Python 3, ``0``-prefixed literals
(except ``0`` itself) are no longer allowed.

You will need to switch to the new syntax in both cases.


* (Tabs and Spaces) - done


New-Style Classes
-----------------

XXX (these aren't necessarily needed)


Rich comparison methods
-----------------------

XXX
XXX: cmp() is missing
XXX: locale.strcoll -> locale.strxfrm

