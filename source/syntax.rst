Syntax Changes
--------------

Python 3 cleaned up some warts of the language's syntax.

The changes needed to accommodate this are mostly mechanical, with
little chance of breaking code, so they work well as the first patches
to send to a project when intending to port it.


.. index:: tabs and spaces

Tabs and Spaces
~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: see below
* Prevalence: Very common (unless the code uses a style linter)

In Python 2, a tab character in indentation was considered equal to 8 spaces
or less.
In Python 3, a tab is only equal to another tab, so the following code is
rejected (whitespace highlighted)::

    def f(cond):
    ····if cond:
    →       do_something()
    ····else:
    →       do_something_else()

If your code mixes tabs and spaces, the easiest way to fix this is
converting all tabs to spaces.
You can use the following Bash command for this::

    find . -name '*.py' -type f -exec bash -c 'T=$(mktemp); expand -i -t 8 "$0" > "$T" && mv "$T" "$0"' {} \;


.. index:: SyntaxError; tuple in argument list

Tuple Unpacking in Parameter Lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf fissix.fixes.fix_tuple_params`` (fixup needed)
* Prevalence: Common

Python 3 requires that each argument of a ``def`` function has a name.
This simplifies code that uses introspection (such as help systems,
documentation generation, and automatic dispatchers), but it does
have a drawback: tuples are no longer allowed in formal parameter lists.

For example, functions like these are no longer allowed in Python 3::

    def line((x1, y1), (x2, y2)):
        connect_points(Point(x1, y1), Point(x2, y2))

    lambda (key, item): (item, key)

The recommended fixer does a good job in finding places that need fixing,
but it does need some manual cleanup.
The above example would be rewritten to::

    def line(xxx_todo_changeme, xxx_todo_changeme1):
        (x1, y1) = xxx_todo_changeme
        (x2, y2) = xxx_todo_changeme1
        connect_points(Point(x1, y1), Point(x2, y2))

    lambda key_item: (key_item[1], key_item[0])

For ``def``, each of the newly introduced variables should be renamed to
something more appropriate.

As for ``lambda``, this transformation can leave the code less readable than
before.
For each such ``lambda``, you should consider if replacing it with a regular
named function would be an improvement.


.. index:: backtick (`), grave operator (`), `; backtick operator

Backticks
~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf fissix.fixes.fix_repr`` (with caveat)
* Prevalence: Common

The backtick (`````) operator was removed in Python 3.
It is confusingly similar to a single quote, and hard to type on some
keyboards.
Instead of the backtick, use the equivalent built-in function :py:func:`repr`.

The recommended fixer does a good job, though it doesn't catch the case where
the name ``repr`` is redefined, as in::

    repr = None
    print(`1+2`)

which becomes::

    repr = None
    print(repr(1+2))

Re-defining built-in functions is usually considered bad style, but it never
hurts to check if the code does it.


.. index:: inequality, diamond operator (<>)
.. index:: <>; inequality operator

The Inequality Operator
~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf fissix.fixes.fix_ne``
* Prevalence: Rare

In the spirit of “There's only one way to do it”, Python 3 removes the
little-known alternate spelling for inequality: the ``<>`` operator.

The recommended fixer will replace all occurrences with ``!=``.


.. index:: None, True, False
.. index:: SyntaxError; None, SyntaxError; True, SyntaxError; False

New Reserved Words
~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Rare

In Python 3, ``None``, ``True`` and ``False`` are syntactically keywords,
not variable names, and cannot be assigned to.
This was partially the case with ``None`` even in Python 2.6.

Hopefully, production code does not assign to ``True`` or ``False``.
If yours does, figure a way to do it differently.

Other Syntax Changes
~~~~~~~~~~~~~~~~~~~~

For convenience and completeness, this section lists syntax changes covered
in other chapters:

* :ref:`print-function`
* :ref:`except-syntax`
* :ref:`raise-syntax`
* :ref:`import-star`
* :ref:`long-literals`
* :ref:`octal-literals`
* :ref:`exec`

.. todo:: complete list
