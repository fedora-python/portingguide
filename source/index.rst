The Conservative Python 3 Porting Guide
=======================================

This document will guide you through porting your software to Python 3.
It is geared towards projects that are being ported because support for
Python 2 is ending in a few years, and less for those that are porting because
Python 3 as a language allows writing expressive, maintainable and correct
code more easily.
It mainly targets projects with large, conservative codebases.

We assume the *maintainers* of the codebase will only grudgingly
accept porting-related changes, not necessarily that *you* specifically have
an aversion to Python 3.
If *you* are not convinced that Python 3 is a good choice, please read the
`foreword of Lennart Regebro's book`_, and skim
Nick Coghlan's `Python 3 Q & A`_, which discusses the issues
(both with Python 2 and 3) in depth.

This guide does *not* cover Python3-only features.
If you're interested in updating your code to take advantage of current
best practices, rather than doing the minimum amount of work necessary to
keep your software working on modern versions of Python, a better resource
for you would be Lennart Regebro's book, `Supporting Python 3`_ (known as
“Porting to Python 3” in earlier editions).

This is an *opinionated* guide. It explains one tried way to do the porting,
rather than listing all alternatives and leaving you to research them
and choose.

Still with us? Let's dive in!


.. toctree::
   :maxdepth: 2

   process
   tools

   syntax
   exceptions
   imports
   stdlib-reorg
   numbers
   strings
   dicts
   iterators
   builtins
   comparisons
   classes
   comprehensions
   core-obj-misc
   etc


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. _Python 3 Q & A: http://python-notes.curiousefficiency.org/en/latest/python3/questions_and_answers.html
.. _foreword of Lennart Regebro's book: http://python3porting.com/foreword.html
.. _Supporting Python 3: http://python3porting.com/
.. _pylint: https://www.pylint.org/
