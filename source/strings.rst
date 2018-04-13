

.. index:: str, bytes, text, unicode

Strings
=======

From a developer's point of view, the largest change in Python 3
is the handling of strings.
In Python 2, the ``str`` type was used for two different kinds of values –
*text* and *bytes*, whereas in Python 3, these are separate and incompatible types.

*

    **Text** contains human-readable messages, represented as a sequence of
    Unicode codepoints.
    Usually, it does not contain unprintable control characters such as NULL.

    This type is available as ``str`` in Python 3, and ``unicode``
    in Python 2.

    In code, we will refer to this type as ``unicode`` – a short, unambiguous
    name, although one that is not built-in in Python 3.
    Some projects refer to it as ``six.text_type`` (from the :ref:`six`
    library).

*

    **Bytes** or *bytestring* is a binary serialization format suitable for
    storing data on disk or sending it over the wire. It is a sequence of
    integers between 0 and 255.
    Most data – images, sound, configuration info, or *text* – can be
    serialized (encoded) to bytes and deserialized (decoded) from
    bytes, using an appropriate protocol such as PNG, VAW, JSON
    or UTF-8.

    In both Python 2.6+ and 3, this type is available as ``bytes``.

Ideally, every “stringy” value will explicitly and unambiguously be one of
these types (or the native string, below).
This means that you need to go through the entire codebase, and decide
which value is what type.
Unfortunately, this process generally cannot be automated.

We recommend replacing the word "string" in developer documentation
(including docstrings and comments) with either “text”/“text string” or
“bytes”/“byte string”, as appropriate.

.. index:: native string

The Native String
-----------------

Additionally, code that supports both Python 2 and 3 in the same codebase
can use what is conceptually a third type:

*

    The **native string** (``str``) – text in Python 3, bytes in Python 2

Custom ``__str__`` and ``__repr__`` methods, and code that deals with
Python language objects (such as attribute/function names) will always need to
use the native string, because that is what each version of Python uses
for internal text-like data.
Developer-oriented texts, such as exception messages, could also be native
strings.

For other data, you can use the native string in these circumstances:

    * You are working with textual data
    * Under Python 2, each “native string” value has a single well-defined
      encoding (such as ``UTF-8`` or :func:`py2:locale.getpreferredencoding`)
    * You do not mix native strings with either bytes or text – always
      encode/decode diligently when converting to these types.

Native strings affect the semantics under Python 2 as little as possible,
while not requiring the resulting Python 3 API to feel bad. But, having
a third incompatible type makes porting process harder.
Native strings are suitable mostly for conservative projects, where ensuring
stability under Python 2 justifies extra porting effort.


.. index:: encode, decode

Conversion between text and bytes
---------------------------------

It is possible to :meth:`~str.encode` text to binary data, or
:meth:`~bytes.decode` bytes into a text string, using a particular encoding.
By itself, a bytes object has no inherent encoding, so it is not possible
to encode/decode without knowing the encoding.

It's similar to images: an open image file might be encoded in PNG, JPG, or
another image format, so it's not possible to "just read" the file
without either relying on external data (such as the filename), or effectively
trying all alternatives.
Unlike images, one bytestring can often be successfully decoded using more
than one encoding.

So, never assume an encoding without consulting relevant documentation
and/or researching a string's use cases.
If an encoding for a particular use case is determined, document it.
For example, a docstring can specify that some argument is “a bytestring
holding UTF-8-encoded text data”.

Some common encodings are:

* ``UTF-8``: A widely used encoding that can encode any Unicode text,
  using one to four bytes per character.
* ``UTF-16``: Used in some APIs, most notably Windows and Java ones.
  Can also encode the entire Unicode character set, but uses two to four bytes
  per character.
* ``ascii``: A 7-bit (128-character) encoding, useful for some
  machine-readable identifiers such as hostnames (``'python.org'``),
  or textual representations of numbers (``'1234'``, ``'127.0.0.1'``).
  Always check the relevant standard/protocol/documentation before assuming
  a string can only ever be pure ASCII.
* ``locale.getpreferredencoding()``: The “preferred encoding” for
  command-line arguments, environment variables, and terminal input/output.


Conversion to text
------------------

There is no built-in function that converts to text in both Python versions.
The :ref:`six` library provides ``six.text_type``, which is fine if it appears
once or twice in uncomplicated code.
For better readability, we recommend using ``unicode``,
which is unambiguous and clear, but it needs to be introduced with the
following code at the beginning of a file::

    if not six.PY2:
        unicode = str


Conversion to bytes
-------------------

There is no good function that converts an arbitrary object to bytes,
as this operation does not make sense on arbitrary objects.
Depending on what you need, explicitly use a serialization function
(e.g. :func:`pickle.dumps`), or convert to text and encode the text.


.. index:: u (string prefix), b (string prefix)

String Literals
---------------

Quoted string literals can be prefixed with ``b`` or ``u`` to get bytes or
text, respectively.
These prefixes work both in Python 2 (2.6+) and 3 (3.3+).
Literals without these prefixes result in native strings.

Add a ``b`` or ``u`` prefix to all strings, unless a native string
is desired.


.. index:: TypeError; mixing text and bytes

String operations
-----------------

In Python 3, text and bytes cannot be mixed.
For example, these are all illegal::

    b'one' + 'two'

    b', '.join(['one', 'two'])

    import re
    pattern = re.compile(b'a+')
    pattern.patch('aaaaaa')


Type checking
-------------

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_basestring``
* Prevalence: Rare

Because the ``str`` and ``unicode`` types in Python 2 could be used
interchangeably, it sometimes didn't matter which of the types a particular
value had. For these cases, Python 2 provided the class :class:`py2:basestring`,
from which both ``str`` and ``unicode`` derived::

    if isinstance(value, basestring):
        print("It's stringy!")

In Python 3, the concept of ``basestring`` makes no sense: text is only
represented by ``str``.

For type-checking text strings in code compatible with both versions, the
:ref:`six` library offers ``string_types``, which is ``(basestring,)``
in Python 2 and ``(str,)`` in Python 3.
The above code can be replaced by::

    import six

    if isinstance(value, six.string_types):
        print("It's stringy!")

The recommended fixer will import ``six`` and replace any uses of
``basestring`` by ``string_types``.


.. index:: file I/O open

.. _str-file-io:

File I/O
~~~~~~~~

* :ref:`Fixer <python-modernize>`: ``python-modernize -wnf libmodernize.fixes.fix_open``
* Prevalence: Common

In Python 2, reading from a file opened by :func:`py2:open` yielded the generic
``str``.
In Python 3, the type of file contents depends on the mode the file was opened
with. By default, this is text strings; ``b`` in mode selects bytes::

    with open('/etc/passwd') as f:
        f.read()  # text

    with open('/bin/sh', 'rb') as f:
        f.read()  # bytes

On disk, all files are stored as bytes.
For text-mode files, their content is decoded automatically.
The default encoding is ``locale.getpreferredencoding(False)``, but this might
not always be appropriate, and may cause different behavior across systems.
If the encoding of a file is known, we recommend always specifying it::

    with open('data.txt', encoding='utf-8') as f:
        f.read()

Similar considerations apply when writing to files.

The behavior of ``open`` is quite different between Python 2 and 3.
However, from Python 2.6 on, the Python 3 version is available in the :mod:`io`
module.
We recommend replacing the built-in ``open`` function with ``io.open``,
and using the new semantics – that is, text files contain ``unicode``::

    from io import open

    with open('data.txt', encoding='utf-8') as f:
        f.read()

Note that under Python 2, the object returned by ``io.open`` has a different
type than that returned by ``open``.
If your code does strict type checking, consult the notes on the
:ref:`file() built-in <file-builtin>`.

The recommended fixer will add the ``from io import open`` import, but it
will not add ``encoding`` arguments.
We recommend adding them manually if the encoding is known.


.. index:: tests; text and bytes

.. _testing-str:

Testing Strings
~~~~~~~~~~~~~~~

When everything is ported and tests are passing, it is a good idea to make
sure your code handles strings correctly – even in unusual situations.

Many of the tests recommended below exercise behavior that
“works” in Python 2 (does not raise an exception – but may produce subtly wrong
results), while a Python 3 version will involve more thought and code.

You might discover mistakes in how the Python 2 version processes strings.
In these cases, it might be a good idea to enable new tests for Python 3 only:
if some bugs in edge cases survived so far, they can probably live until
Python 2 is retired. Apply your own judgement.

Things to test follow.


Non-ASCII data
..............

Ensure that your software works (or, if appropriate, fails cleanly)
with non-ASCII input, especially input from end-users.
Example characters to check are:

* ``é ñ ü Đ ř ů Å ß ç ı İ`` (from European personal names)
* ``Ａ ﬄ ℚ ½`` (alternate forms and ligatures)
* ``€ ₹ ¥`` (currency symbols)
* ``Ж η 글 ओ କ じ 字`` (various scripts)
* ``🐍 💖 ♒ ♘`` (symbols and emoji)


Encodings and locales
.....................

If your software handles multiple text encodings, or handles user-specified
encodings, make sure this capability is well-tested.

Under Linux, run your software with the ``LC_ALL`` environment variable
set to ``C`` and ``tr_TR.UTF-8``, and check handling of any command-line
arguments and environment variables that may contain non-ASCII characters.


Invalid input
.............

Test how the code handles invalid text input.
If your software deals with files, try it a on non-UTF8 filename.

Using Python 3, such a file can be created by::

    with open(b'bad-\xFF-filename', 'wb') as file:
        file.write(b'binary-\xFF-data')
