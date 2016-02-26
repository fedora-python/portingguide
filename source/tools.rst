Tools
=====

Several tools exist to automate as much of the porting as possible,
and to check for common errors.
Here is a survey of tools we reccommend.


six
---

When porting a large piece of software, it is desirable to support both
Python 2 and Python 3 in the same codebase.
Many projects will need this dual support for a long time,
but even those that can drop Python 2 support as soon as the port is done
will typically go through a period of adding Python 3 support,
in which the software should continue to work on Python 2.

Six makes it practical to write such version-straddling code
by offering compatibility wrappers over the differences.

For example, the Python 3 syntax for specifying metaclasses is not valid
Python 2, ande the Python 2 way does nothing in Python 3,
so ``six`` provides an ``add_metaclass`` decorator for this purpose.
It also provides stable names for standard library modules that were
moved or reorganized in Python 3.

Six is a run-time dependency, albeit a very small one.
If your project is unfriendly to third-party dependencies, push for this
one as hard as possible.
If you do not use ``six``, you will most likely end up reimplementing it
or outright copying relevant pieces of it into your code.


modernize
---------

XXX


sixer
-----

XXX


py3c
----

XXX


pylint --py3k
-------------

XXX
