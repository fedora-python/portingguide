Other Changes
-------------

This page documents a few miscellaneous topics at the edges of this guide's
scope: low-level buffers, doctests, and bytecode cache files.



Raw buffer protocol: ``buffer`` and ``memoryview``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Very rare

Python 2 used a `buffer`_ interface for sharing blocks of memory between Python
objects and other libraries.

The buffer object and the `corresponding C API`_ proved inaequate, and over
Python 2.6 and 2.7, a new mechanism was implemented: the `Py_buffer`_
structure and the :class:`memoryview` object.

In Python 3, the buffer object and the related C API is removed.

Unfortunately, the specifics of low-level interfaces between Python and
non-Python libraries are too different across projects for us to offer
universal advice on porting to the new API.
If your code uses ``buffer`` (or the ``PyBuffer`` C API), you will need to
refer to the `Python documentation`_ for details, and combine that with
knowledge about your particular interface.

.. _buffer: https://docs.python.org/2/library/functions.html#buffer
.. _corresponding C API: https://docs.python.org/2/c-api/objbuffer.html
.. _Py_buffer: https://docs.python.org/3/c-api/buffer.html
.. _Python documentation: https://docs.python.org/2/c-api/buffer.html

Doctests
~~~~~~~~

* :ref:`Fixer <python-modernize>`: None
* Prevalence: Common

`Doctests`_ are a common practice for quick tests and testing documentation.
They work by extracting snippets example code and its output in documentation,
running the code, and verifying that its result matches, textually, the example
output.

This relies on minute details of textual representation of Python objects,
which is generally not under any backwards-compatibility guarantee and may
change at any time – even across minor versions of Python (e.g. 2.6 to 2.7 or
3.5 to 3.6).

.. note::
    Some examples of what changed between Python 2 and 3 are:

    * String have different ``u`` and ``b`` prefixes depending on if they're
      bytes or text.
    * Large integers lost the ``L`` suffix.
    * The order of items in dictionaries may be different (and unpredictable).

Doctests are a good way to ensure that the *documentation* is correct (i.e.
it doesn't contain broken examples), but they are *not* a good way to actually
test the code.

If your code uses doctests as the main means of testing, rewrite them as tests
that do not rely on exact textual output.
You can use the built-in :mod:`unittest`, or the third-party `pytest`_ library,
among others.

Once your doctests are only testing documentation, we recommend the following
strategy:

* Keep running doctests under Python 2
* Port all code to be compatible with (and tested on) both Python 2 and 3
* At one moment, update examples in the docs, and start only using Python 3
  to run the doctests.

Since the code is tested elsewhere, it generally does not matter that code
examples are tested under only one of the supported Python versions.


.. _Doctests: https://docs.python.org/3/library/doctest.html
.. _pytest: https://docs.pytest.org


Reorganization of ``.pyc`` files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since compiling Python code is a relatively expensive operation, and many modules
do not change often, Python caches compiled bytecode in ``.pyc`` files.

In Python 2, ``.pyc`` files were written in the same directory as the
corresponding ``.py`` source files, with only a ``c`` added to the filename.
The exact mechanism had two major drawbacks:

* Bytecode is not compatible across Python versions.
  If the same module was being imported by different versions of Python,
  each would overwrite the ``.pyc`` file with its own flavor of bytecode on
  import. This would invalidating the cache for all other versions.
* The ``.pyc`` cache could be used even without a corresponding ``.py`` file,
  which allowed some space saving (by distributing only the compiled file).
  However, if one deleted a ``.py`` file but forgot to also remove the ``.pyc``,
  Python would act as if the module was still present.
  This was quite confusing, especially for beginners.

Python 3 puts ``.pyc`` files in a separate directory called ``__pycache__``,
and adds version information to the filename.
The new mechanism avoids the above two problems: per-version caches are
separated, and if the ``.py`` source is missing, the ``.pyc`` file is not
considered.

If your code relies on the location of ``.pyc`` files (for example, if
your build/packaging system doesn't handle Python 3), you will need to update
to the new location.

If you rely on importing ``.pyc`` files without corresponding source,
you will need to move the ``.pyc`` to the old location, and remove the
version tag. For example, move::

    __pycache__/foo.cpython-36.pyc

to::

    foo.pyc

Under this name, the ``.pyc`` will be recognized by Python 3's import
machinery.
