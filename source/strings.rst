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

    In code, we will refer to this type as ``unicode`` – a short, unabmbiguous
    name, although one that is not built-in in Python 3.
    Some projects refer to it as ``six.text_type`` (from the :ref:`six`
    library).

*

    **Bytes** or *bytestring* is a binary serialization format suitable for
    storing data on on disk or sending it over the wire. It is a sequence of
    integers between 0 and 255.
    Most data – images, sound, configuration info, or *text* – can be
    serialized (encoded) to bytes and deserialized (decoded) from
    bytes, using an appropriate protocol such as PNG, VAW, JSON
    or UTF-8.

    In both Python 2.6+ and 3, this type is available as ``bytes``.

Ideally, every “stringy” value will explicitly and unambiguously be one of
these types (or the native string, below).
This means that you need to go through the entire codebase, and decide
these two types.
Unfortunately, this process generally cannot be automated.

We recommend replacing the word "string" in developer documentation
(e.g. docstrings) with either “text”/“text string” or “bytes”/“byte string”,
as appropriate.

The Native String
-----------------

Additionally, code that supports both Python 2 and 3 in the same codebase
can use what is conceptually a third type:

*

    The **native string** (``str``) – text in Python 3, bytes in Python 2

Custom ``__str__`` and ``__repr__`` methods, and code that deals with
Python language objects (such as atribute/function names) will always need to
use the native string, because that is what each version of Python uses
for text-like data.

For other data, you can use the native string in these circumstances:

    * You are working with textual data
    * Under Python 2, each “native string” value has a well-defined encoding
      (such as ``UTF-8`` or :func:`py2:locale.getpreferredencoding`)
    * You do not mix native strings with either bytes or text – always
      encode/decode dilligently when converting to these types.

Native strings affect the semantics under Python 2 as little as possible,
while not requiring the resulting Python 3 API to feel bad. But, adding
a third incompatible type makes porting process harder, so it is suitable
mostly for conservative projects.


Conversion between text and bytes
---------------------------------

It is possible to *encode* text to binary data, or *decode* bytes into
a text string, using a particular encoding.
By itself, a bytes object has no inherent encoding, so it is not possible
to encode/decode without knowing the encoding.

It's similar to images: an open image file might be encoded in PNG, JPG, or
another image format, so it's not possible to "just read" the file
without either relying on external data (such as the filename), or effectively
trying all alternatives.
Unlike images, one bytestring can often be successfully decoded using more
than one encoding.

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
  a string can only be pure ASCII.
* ``locale.getpreferredencoding()``: The “preferred encoding” for
  command-line arguments, environment variables, and terminal input/output.


Conversion to text or bytes
---------------------------

There is no built-in function that converts to text in both Python versions.
The :ref`six` library provides ``six.text_type``, which is fine if it appears
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


String Literals
---------------

Quoted string literals can be prefixed with ``b`` or ``u`` to get bytes or
text, respectively.
These prefixes work both in Python 2 (2.6+) and 3 (3.3+).
Literal without these prefixes result in native strings.


String operations
-----------------

In Python 3, text and bytes can not be mixed.
For example, these are all illegal::

    b'one' + 'two'

    b', '.join(['one', 'two'])

    import re
    pattern = re.compile(b'a+')
    pattern.patch('aaaaaa')


Type checking
-------------




The New File I/O Stack
~~~~~~~~~~~~~~~~~~~~~~
