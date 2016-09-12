Dictionaries
------------

There are two most significant changes related to dictionaries in Python 3.

``dict.has_key()``
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf lib2to3.fixes.has_key``
* Prevalence: Common

``dict.has_key()`` method is no longer available in Python 3.

Instead of::

    dictionary.has_key('keyname')

you should use::

    'keyname' in dictionary

Dict Views and Iterators
~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_dict_six``
* Prevalence: Common

Methods ``dict.iterkeys()``, ``dict.iteritems()`` and ``dict.itervalues()`` are
no longer supported.

Methods ``dict.keys()``, ``dict.items()`` and ``dict.values()`` return view
instead of list. So, if you need to work with list - for example to obtain list
of sorted keys from dictionary - instead of::

    keys = dictionary.keys()
    keys.sort()

you now should use this::

    keys = sorted(dictionary)

Mentioned fixer takes care about usage of this methods. For example this code::

    for k in dictionary.keys():
        print(k)

    print(dictionary.keys())
    print(dictionary.items())
    print(dictionary.values())

is modified to::

    for k in dictionary.keys():
        print(k)

    print(list(dictionary.keys()))
    print(list(dictionary.items()))
    print(list(dictionary.values()))

As you can see, in ``for`` loop is better to use iterator so fixer doesn't
change it to list, but in ``print`` it does.

This fixer also solves issues with unsupported methods. For example methods::

    print(dictionary.iterkeys())
    print(dictionary.iteritems())
    print(dictionary.itervalues())

are modified to::

    print(six.iterkeys(dictionary))
    print(six.iteritems(dictionary))
    print(six.itervalues(dictionary))
