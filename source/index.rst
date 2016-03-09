The Conservative Python 3 Porting Guide
=======================================

.. note::

    This guide is in *outline* stage. The details are not fleshed out.

This document will guide you through porting your software to Python 3.
It is geared towards projects that are ported because support for Python 2
is ending in a few years, and less for those where that are porting because
Python 3 as a language allows writing expressive, maintainable and correct
code more easily.
It mainly targets projects with large, conservative codebases.

We assume the *maintainers* of the codebase will only grudgingly
accept porting-related changes, not necessarily that *you* specifically have
an aversion to Python 3.
If *you* are not convinced that Python 3 is a good choice, please skim
Nick Coghlan's `Python 3 Q & A`_, which discusses the issues
(both with Python 2 and 3) in depth.

If you're interested in *updating* your code to take advantage of current
best practices, rather than doing the minimum amount of work necessary to
keep your software working on modern versions of Python, a better resource
for you would be Lennart Regebro's book, `Supporting Python 3`_ (known as
“Porting to Python 3” in earlier editions).

This is an *opinionated* guide. It explains one tried way to do the porting,
rather than listing all alternatives and leaving you to research them
and choose.

Still with us? Let's dive in!

The porting process
===================

*   :doc:`Make sure you have tests <tests>`

    First, your software needs to be tested.
    It is practically impossible to change untested software.

*   :doc:`Familiarize yourself with porting tools <tools>`

    Read up on the roles of ``six``, ``sixer``, ``modernize``,
    ``py3c`` and ``pylint --py3k``.

*   :doc:`Define data types you are using <types>`

    The biggest change in Python 3 is handling of the string types.
    Python 3 draws a sharp distinction between *text* and *bytes*,
    and requires that conversions between these are made explicitly,
    with a well-defined encoding.

    Before porting, it helps to decide, on a big-picture scale,
    which data is textual and which is bytes.

    Also, static type-checking tools are available to help the porting
    process.

*   **Modernize** your code

    Migrate away from deprecated features that have a Python3-compatible
    equivalent backported to Python 2.
    In this step, you will drop support for Python 2.5 and lower.

*   **Port** your code

    Add support for Python 3 while keeping compatibility with Python 2.

*   **Clean up** (optional)

    After you decide to drop support for Python 2, you can remove
    compatibility workarounds, and start using Python 3 features.

    This section is included for completeness, since it is not strictly
    necessary to modify code that is already working under
    both major Python versions.


.. toctree::
   :maxdepth: 2

   tests
   tools
   types

.. comment:

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

.. _Python 3 Q & A: http://python-notes.curiousefficiency.org/en/latest/python3/questions_and_answers.html
.. _Supporting Python 3: http://python3porting.com/
.. _pylint: https://www.pylint.org/
