======================
Support For Python 3.X
======================

What Versions Support Python 3.X
--------------------------------

Only mod_wsgi version 3.0 and later supports Python 3.X.

Compatible Versions Of Python 3.X
---------------------------------

Python 3.0 will not be supported, you will need to at least be using Python
3.1 if you want to use Python 3.X at all. This is in part because it is
assumed the PSF itself would prefer people not to use Python 3.0, but also
because code is relying on 'surrogateescape' mechanisms from PEP 383 and
this was only added in Python 3.1.

WSGI Specification And Python 3.X
---------------------------------

Note that Python 3 support in mod_wsgi is compatible with
`PEP 3333 <http://www.python.org/dev/peps/pep-3333/>`_ except for the value
of 'wsgi.version'. Apache/mod_wsgi also allows some responses which PEP 3333
forbids. So long as you code to PEP 3333 the latter should not be an issue.
The next major version of Apache/mod_wsgi will be stricter on what it
allows to ensure people write portable code for Python 3.

There is as yet still no official update to the WSGI specification
indicating how Python 3.X should implement it. A defacto definition of what
WSGI 1.0 should look like for Python 3.X has emerged however due to what
the development versions of mod_wsgi 3.0 and the 'wsgiref' module in the
Python standard library implemented, albeit that 'wsgiref' may not be usable
due to issues in separate modules it relies upon.

The keys points in respect of how the WSGI 1.0 specification has been
reinterpreted is as follows:

1. The application is passed an instance of a Python dictionary containing
what is referred to as the WSGI environment. All keys in this dictionary
are native strings. For CGI variables, all names are going to be ISO-8859-1
and so where native strings are unicode strings, that encoding is used for
the names of CGI variables.

2. For the WSGI variable 'wsgi.url_scheme' contained in the WSGI
environment, the value of the variable should be a native string.

3. For the CGI variables contained in the WSGI environment, the values of
the variables are native strings. Where native strings are unicode strings,
ISO-8859-1 encoding would be used such that the original character data is
preserved and as necessary the unicode string can be converted back to
bytes and thence decoded to unicode again using a different encoding.

4. The WSGI input stream 'wsgi.input' contained in the WSGI environment and
from which request content is read, should yield byte strings.

5. The status line specified by the WSGI application should be a byte
string. Where native strings are unicode strings, the native string type
can also be returned in which case it would be encoded as ISO-8859-1.

6. The list of response headers specified by the WSGI application should
contain tuples consisting of two values, where each value is a byte string.
Where native strings are unicode strings, the native string type can also
be returned in which case it would be encoded as ISO-8859-1.

7. The iterable returned by the application and from which response content
is derived, should yield byte strings. Where native strings are unicode
strings, the native string type can also be returned in which case it would
be encoded as ISO-8859-1.

8. The value passed to the 'write()' callback returned by 'start_response()'
should be a byte string. Where native strings are unicode strings, a native
string type can also be supplied, in which case it would be encoded as
ISO-8859-1.

WSGI Interface Version Identifier
---------------------------------

Note that at this time, for where either Python 2.X or 3.X is used,
mod_wsgi 3.0 is defining the 'wsgi.version' tuple in the WSGI environment
as '(1, 1)' rather than '(1, 0)' as the WSGI PEP 333 specification
requires.

This was being done as a way of trying to push for an update of the WSGI
specification to at least address the issue that the 'readline()' function
of 'wsgi.input' needs to be able to accept a size hint. This is necessary
as 'cgi.FieldStorage' in the Python standard library passes such a hint,
yet WSGI 1.0 does not require a WSGI adapter to accept it. Because that
class in standard library is used by many applications/frameworks, all
were actually in violation of the WSGI specification.

It was also the intent to try and push for a number of other changes and
additional requirements on WSGI adapters and middleware. The simplified
list of all such changes was:

1. The 'readline()' function of 'wsgi.input' must optionally take a size
hint.

2. The 'wsgi.input' functions for reading input must return an empty string
as end of input stream marker.

3. The size argument to 'read()' function of 'wsgi.input' is optional
and if not supplied the function would return all available request
content.

4. Any WSGI application or middleware should not itself return, or consume
from a wrapped WSGI component, more data than specified by the
Content-Length response header if defined.

5. The WSGI adapter must not pass on to the server any data above what the
Content-Length response header defines if supplied.

Support on getting these changes to WSGI specification made has though
now been withdrawn, although looks like others may follow up on it still,
with though (3) likely being dropped.

If that doesn't happen however, a new version of mod_wsgi will likely be
soon released which reverts the 'wsgi.version' tuple back to '(1, 0)' to be
conformant with WSGI PEP 333.
