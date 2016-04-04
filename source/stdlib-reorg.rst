Standard Library Reorganization
-------------------------------

The standard library has been reorganized for Python 3.

Renamed Modules
~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_imports_six``
* Prevalence: Common

Many modules were simply renamed, usually to unify file naming conventions
(e.g. :mod:`py2:ConfigParser` to :mod:`configparser`) or to consolidate related
modules in a namespace (e.g. :mod:`py2:tkFont` to :mod:`tkinter.font`).

The :ref:`six` library includes ``six.moves``, a pseudo-package that exposes
moved modules under names that work in both Python 2 and 3.
For example, instead of::

    from ConfigParser import ConfigParser

you should import ``six.moves``::

    from six.moves.configparser import ConfigParser

A list of all renamed modules is included in `six documentation`_.

The recommended fixer will automatically change imports to use ``six.moves``.

.. _six documentation: https://pythonhosted.org/six/#module-six.moves

.. todo:: copy list here, to fill the index


Removed modules
~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Uncommon

Some modules have been removed entirely.
Usually, these modules were supplanted by better alternatives
(e.g. :mod:`py2:mimetools` by :mod:`email`),
specific to now-unsupported operating systems (e.g. :mod:`py2:fl`),
or known to be broken (e.g. :mod:`py2:Bastion`).

Lennart Regebro compiled a list of these modules in the book
„Supporting Python 3”, which is `available online <http://python3porting.com/stdlib.html#removed-modules>`_.

If your code uses any of the removed modules, check the *Python 2*
documentation of the specific module for recommended replacements.

.. todo:: copy list here, to fill the index


The ``urllib`` module
~~~~~~~~~~~~~~~~~~~~~

.. todo:: urllib


The ``string`` module
~~~~~~~~~~~~~~~~~~~~~

.. todo:: string
