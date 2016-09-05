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

A list of all renamed modules is included in
`six documentation <https://pythonhosted.org/six/#module-six.moves>`_.

The recommended fixer will automatically change imports to use ``six.moves``.

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
“Supporting Python 3”, which is `available online <http://python3porting.com/stdlib.html#removed-modules>`_.

If your code uses any of the removed modules, check the *Python 2*
documentation of the specific module for recommended replacements.

.. todo:: copy list here, to fill the index


.. index:: urllib, urllib2, urlparse

The ``urllib`` modules
~~~~~~~~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Common

The :mod:`py2:urllib`, :mod:`py2:urllib2` and :mod:`py2:urlparse` modules were
reorganized more heavily, with individual functions and classes reistributed to
submodules of Python 3's :mod:`urllib`: :mod:`urllib.parse`, :mod:`urllib.error`,
:mod:`urllib.request`, and :mod:`urllib.response`.

These functions are included in ``six.moves``, and the
`six documentation <https://pythonhosted.org/six/#module-six.moves.urllib.parse>`_
has details on what moved where.
Use this information to adjust your code.

The ``fix_imports_six`` does not handle all urllib moves.

.. todo:: copy list here, to fill the index


The ``string`` module
~~~~~~~~~~~~~~~~~~~~~

* Fixer: None
* Prevalence: Rare

In Python 2, the ``string`` module included functions that mirrored ``str``
methods, such as :func:`py2:string.lower` and :func:`py2:string.join`
that mirror :meth:`str.lower` and :meth:`str.join`.
These have been deprecated since Python 2.4, and they are removed in Python 3.

Convert all uses of these functions to string methods.

For example, this code::

    import string
    products = ['widget', 'thingy', 'whatchamacallit']
    print string.join(products, sep=', ')

should be replaced with::

    products = ['widget', 'thingy', 'whatchamacallit']
    print(', '.join(products))

The :ref:`python-modenize` tool doesn't provide an automated fixer for these
changes.

.. todo:: copy list here, to fill the index
