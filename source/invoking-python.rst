Invoking Python
---------------

While this is not a change in Python 3, the transition increased the number of
systems that have more than one Python interpreter installed: it is not
uncommon for ``python``, ``python2``, ``python3``, ``python3.6`` and
``python3.9`` to all be valid system commands; other interpreters maay be
installed in non-standard locations.

This makes it important to use the correct command for each situation.


Current interpreter
~~~~~~~~~~~~~~~~~~~

The current Python interpreter should be invoked via ``sys.executable``.

Python provides the filename of the currently running interpreter as
:data:`sys.executable`.
This variable should be preferred over ``python`` or other hard-coded commands.

For example, rather than::

    subprocess.Popen('python', 'somescript.py')

use::

    subprocess.Popen(sys.executable, 'somescript.py')

The assumption that ``'python'`` is correct is only valid in tightly controlled
environments; however, even in those environments ``sys.executable`` is likely
to be correct.

The documentation does include a warning:

   If Python is unable to retrieve the real path to its executable,
   ``sys.executable`` will be an empty string or ``None``.

In practice, this does not apply to mainstream platforms.
If ``sys.executable`` is unusable, then either your platform's concept of
launching a process via filename is somehow unusual (and in this
case you should know what to do), or there's an issue in Python itself.


Unix shebangs
~~~~~~~~~~~~~

On Unix, executables written in Python must have a shebang line identifying
the interpreter.
The correct shebang to use will depend on the environment you are targeting
and on the version compatibility of the project.

General recommendations for Pytohn shebangs are listed in
the `For Python script publishers`_ section of PEP 394.

.. _For Python script publishers: https://www.python.org/dev/peps/pep-0394/#for-python-script-publishers
