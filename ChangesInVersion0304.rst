

======================
Changes In Version 3.4
======================

Working version of mod_wsgi 3.4 can currently only be obtained by checking
it out from the source code repository. The Mercurial command you should
use is:

::

    hg clone -b mod_wsgi-3.X http://modwsgi.googlecode.com/hg/ mod_wsgi-3.X


Bugs Fixed
----------

1. If using write() function returned by start_response() and a non string
value is passed to it, then process can crash due to errors in Python object
reference counting in error path of code.

2. If using write() function returned by start_response() under Python 3.X
and a Unicode string is passed to it rather than a byte string, then a
memory leak will occur because of errors in Python object reference
counting.

3. Debug level log message about mismatch in content length generated was
generated when content returned less than that specified by Content-Length
response header even when exception occurring during response generation
from an iterator. In the case of an exception occuring, was only meant to
generate the log message if more content returned than defined by the
Content-Length response header.

New Features
------------

1. Support use of Python 3.2.
