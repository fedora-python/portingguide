Python 2 and Python 3 compatibility
===================================

The both Python 2 and Python 3 codes of the same software will be required for some time. There can be used two strategies how to cover the requirement:

1. Separate branches for Python 2 and Python 3

This strategy makes porting easier. It can be automated by porting tools. There are also avoided compatibility issues between the both Python major releases in the same source code. However, it is more complicated to maintain and develop two separate branches.

2. One source code compatible with Python 2 and Python 3

The strategy can be preferred, if there is required to avoid development and maintenance of two separated branches in Python 2 and Python 3. In this case, the porting will require more investment to keep the compatibility with the both major releases, and also to drop compatibility with Python 2.5 and lower versions.


Libraries
---------

``modernize`` and other tools are able to cover mostly changes related to reorganizations and renamings of libraries in Python 3 by using ``six`` module. Another way is to avoid `six`` module and take advices from ``modernize`` and other tools for new libraries, but they can't be used as such. Regebro's book, `Supporting Python 3`_, describes the changes and principles, how it can be solved in the source code. Some additional examples are here:

Original Python 2 code:

``from StringIO import StringIO``

Advice from ``modernize`` tool:

``from io import StringIO``

Final code compatible with Python 2 and Python 3:

``# Try Python 2 import; if ImportError occurs, use Python 3 import``
``try:``
``    from StringIO import StringIO``
``except ImportError:``
``    from io import StringIO``

There can be other case where can be used a similare solution:

Original Python 2 code:

``from mock import Mock``

Advice from ``modernize`` tool:

``from unittest.mock import Mock``

Final code compatible with Python 2 and Python 3 where is reversed the order of versions:

``# Try Python 3 import; if ImportError occurs, use Python 2 import``
``try:``
``    from unittest.mock import Mock``
``except ImportError:``
``    from mock import Mock``

Other cases can be fixed by following way:

Original Python 2 code:

``from nose.tools import assert_items_equal``

Advice from ``modernize`` tool:

``from nose.tools import assert_count_equal as assert_items_equal``

and changes of ``assert_count_equal`` to ``assert_items_equal`` in the source code.

Final code compatible with Python 2 and Python 3 where the original ``assert_count_equal`` usage is kept in the source code further:

``# Try Python 2 import; if ImportError occurs, use Python 3 import``
``try:``
``    from nose.tools import assert_items_equal``
``except ImportError:``
``    from nose.tools import assert_count_equal as assert_items_equal``


Strings
-------

TBD
