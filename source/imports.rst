Importing
---------

Python 3 brings a complete overhaul of the way ``import`` works,
but developer-visible changes can be summarised as follows.


Absolute imports
~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.fix_import`` (See caveat below)
* Prevalence: Common
* Future import: ``from __future__ import absolute_imports``
* Specification: `PEP 328 <https://www.python.org/dev/peps/pep-0328/>`_

Under Python 2, when importing from inside a package, the package's own modules
were considered before global ones.
For example, given a package like this::

    mypkg/
        __init__.py
        collections.py
        core.py
        ...

If ``core.py`` contains::

    from collections import deque

it would import the ``deque`` from ``collections.py``.
The standard library's ``collections`` module would be unavailable.

In Python 2.5, the situation began changing with the introduction of explicit
relative imports, using a dot (``.``) before the submodule name.
Given the structure above, these statements would be equivalent
(in ``core.py``)::

    from .collections import deque
    from mypkg.collections import deque

Additionally, a *future import* was added to make all imports absolute
(unless explicitly relative)::

    from __future__ import absolute_imports

Using this feature, ``from collections import deque`` will import from
the standard library's ``collections`` module.

.. todo:: Link future import

In Python 3, the feature becomes the default.

To prepare for this, make sure all imports are either absolute, or *explicitly*
relative.
Both the ``mypkg.collections`` style and the ``.collections`` style are
adequate; we recommend the former for increased readability [#f1]_.

The recommended fixer simply adds the future import to all files that
do a potentially ambiguous import.
This may be too much churn for your project; in most cases it is enough to
verify that your imports are not ambiguous.


.. _import-star:

``import *`` in Functions
~~~~~~~~~~~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Rare

In Python 3, “star imports” are only allowed on the module level, not in
classes or functions.
For example, this won't work::

    def coords(angle, distance):
        from math import *
        return distance * cos(angle), distance * sin(angle)

The reason for this limitation is that a function's local variables are
optimized at compile time, but the names imported via ``*`` are not known
in advance.
Python 2 reverted to using unoptimized bytecode for such functions;
Python 3 includes only the optimized case.

This code raised a :py:class:`SyntaxWarning` already in Python 2.6.
In Python 3, this becomes a :py:class:`SyntaxError`, so module-level
test coverage is enough to spot the error.


Import Cycles
~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Rare

Python 3 introduced a reworked importmentation of ``import`` in the form
of the :py:mod:`importlib` module.
The new machinery is backwards-compatible in practice, except that some
import cycles, especially those involving submodules, now raise
:py:class:`ImportError`.

If you encounter such errors, check for import cycles (these should be visible
from the traceback as one module imported multiple times).
In most cases you can break circular imports by refactoring common code into
a separate module.

.. todo:: Elaborate


.. rubric:: Footnotes

.. [#f1] The downside of spelling out the package name is that it becomes
   harder to rename or reorganize the package.
   In practice, the added work tends to be insignificant compared to updating
   all external modules that import your package.
