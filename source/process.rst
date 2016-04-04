The Porting Process
-------------------

This chapter documents the entire process of porting a conservative project
to Python 3.
We recommend that you read it before you embark on your first porting project.


Make Sure your Dependencies are Ported
......................................

Before you start porting, any libraries that your code imports need to run
with Python 3.
Check if this is the case.

Some projects took advantage of the backwards incompatible upgrade to clean
up their interfaces.
For any libraries that are ported already, look in their documentation for
any notes specific to Python 3, and if you find any, note them for later.

If you depend on a library that is not ported, inquire of its authors about
the porting status.
If the library is open-source, consider helping to port it – the experience
will likely help in your own project.
If authors are unwilling to port to Python 3, or if the library is
unmaintained, start looking for a replacement.
For projects in Fedora, the `portingdb`_ project lists known alternatives
for dropped packages.

.. _portingdb: https://fedora.portingdb.xyz


Run the Tests
.............

It's impractical to make any changes to an untested code, let alone porting
the entire codebase to a new version of the programming language.

If the project has automatic tests, run them under Python 2 to make sure
they pass.
If not, write them – or you'll need to resort to testing manually.


Drop Python 2.5 and Lower
.........................

Python 2.6 and 2.7 were released in lockstep with the early 3.x version,
and contain several features that make supporting both versions
possible in the same codebase.

Python 2.5 has been unmaintained for several years now, so any *new* code
written for it does not have much of a future.
Bring this up with the software's maintainers.

If compatibility with Python 2.5 is *really* necessary, we recommend that
you fork the codebase, i.e. work on a copy and regularly merge in any
new development.


Use The Tools
.............

The :doc:`tools` chapter describes a selection of tools that can automate or
ease the porting process, and warn about potential problems or common
regressions.
We recommend that you get familiar with these tools before porting any
substantial project.

In particular, this guide includes „fixers” where appropriate.
These can automate a lot, if not most, of the porting work.
But please read the
:ref:`notes for the python-modernize tool <python-modernize>` before running
them to avoid any surprises.


Port Small Pieces First
.......................

If the codebase contains a small, self-contained module, port it first
before moving on to larger pieces or the entire code.


One Change per Commit
.....................

For changes that are mechanical, and easily automated, we recommend that
you do only one type of change per commit/patch.
For example, one patch to change the :ref:`except syntax <except-syntax>`,
then another for the :ref:`raise syntax <raise-syntax>`.
Do not submit a single patch saying “Port to Python 3”.
Following this workflow makes the changes much easier to review.

The descriptions of individual items in this guide are written so that you
can use them in commit messages with minimal changes to explain why each change
is necessary and to link to more information.


The Rest of this Guide
......................

The next chapter, :doc:`tools`, explains how to automate porting and checking.

Each of the subsequent chapters explains one area where Python 3 differs from
Python 2, and how to adapt the code.
The chapters are arranged roughly according to the order in which they are
usually tacked in a typical project.

We recommend that you skim the introduction of each of the chapters,
so that you know what you're up against before you start.

Happy porting!
