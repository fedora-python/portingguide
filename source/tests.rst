Tests
=====

As with any refactoring, before starting to port to Python 3, you should
ensure your project is adequately tested.
Without tests, any change leads to unexpected (and unnoticed) breakage.

If writing tests specifically for Python 3 porting, there are a few areas
to focus on.


Text handling
-------------

By far the biggest change in Python 3 is the new string model.
It's important to test string-related behavior.

It's possible that you'll find bugs in the existing code.
Before fixing them, consider that the fixes for Python 2 and
Python 3 will most likely be different.
Depending on your porting timeline, it might be preferrable to only
fix them in the ported version.

Many of the tests recommended below exercise behavior that
“works” (as in, “does not raise an exception”) in Python 2,
while a Python 3 version will involve more thought and code.

The porting process is a good time to (re-)evaluate what behavior is
appropriate in various edge cases.
(Though of course, matching existing behavior is the more
conservative option.)


Non-ASCII data
..............

Ensure that your software works (or, if appropriate, fails cleanly)
with non-ASCII input, especially input from end-users.
Example characters to check are:

* ``é ñ ü Đ ř ů Å ß ç`` (from European personal names)
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
