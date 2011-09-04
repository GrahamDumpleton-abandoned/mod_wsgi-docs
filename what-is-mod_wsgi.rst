=================
What Is mod_wsgi?
=================

The mod_wsgi package implements a simple to use Apache module which can
host any Python application which supports the Python WSGI_ interface. The
module is suitable for use in hosting high performance production web
sites, as well as your average self managed personal sites running on a
virtual private server or shared host.

Modes Of Operation
------------------

When hosting WSGI applications using mod_wsgi, one of two primary modes of
operation can be used. In 'embedded' mode, mod_wsgi works in a similar way
to mod_python in that the Python application code will be executed within
the context of the normal Apache child processes. WSGI applications when
run in this mode will therefore share the same processes as other Apache
hosted applications using Apache modules for PHP and Perl.

An alternate mode of operation available with Apache 2.X on UNIX is
'daemon' mode. This mode operates in similar ways to FASTCGI/SCGI
solutions, whereby distinct processes can be dedicated to run a WSGI
application. Unlike FASTCGI/SCGI solutions however, neither a separate
process supervisor or WSGI adapter is needed when implementing the WSGI
application and everything is handled automatically by mod_wsgi.

Because the WSGI applications in daemon mode are being run in their own
processes, the impact on the normal Apache child processes used to serve up
static files and host applications using Apache modules for PHP, Perl or
some other language is much reduced. Daemon processes may if required also
be run as a distinct user ensuring that WSGI applications cannot interfere
with each other or access information they shouldn't be able to.

Note that although mod_wsgi has features similar to FASTCGI/SCGI solutions,
it isn't intended to be a replacement for those hosting mechanisms in all
situations for Python web hosting. Specifically, mod_wsgi is not designed
for nor intended for use in over allocated shared mass virtual hosting
setups for different users on a single Apache instance. For such mass
virtual hosting arrangements, FASTCGI in particular would still be the
preferred choice in most situations.

Server Performance
------------------

The mod_wsgi module is written in C code directly against the internal
Apache and Python application programming interfaces. As such, for hosting
WSGI applications in conjunction with Apache it has a lower memory overhead
and performs better than existing WSGI adapters for mod_python or
alternative FASTCGI/SCGI/CGI or proxy based solutions.

Although embedded mode can technically perform better, daemon mode would
generally be the safest choice to use. This is because to get the best
performance out of embedded mode you must tune the Apache MPM settings,
which in their default settings are biased towards serving of static media
and hosting of PHP applications. If the Apache MPM settings are not set
appropriately for the type of application being hosted, then worse
performance can be seen rather than better performance.

Thus, unless you are adept at configuring Apache, always use daemon mode
when available. Overall, for large Python web applications you wouldn't
normally expect to see any significant difference between daemon mode and
embedded mode, as the bottlenecks are going to be in the Python web
application or any database access.

Supported Applications
----------------------

As mod_wsgi supports the WSGI interface specification, any Python web
framework or application which is compatible with the WSGI interface
specification should be able to be hosted on top of mod_wsgi.

System Requirements
-------------------

The mod_wsgi package can be compiled for and used with either Apache 1.3,
2.0 or 2.2 on UNIX systems (including Linux), as well as Windows. Either
the single threaded 'prefork' or multithreaded 'worker' Apache MPMs can be
used when running on UNIX.

Daemon mode of mod_wsgi will however only be available on Apache 2.0 or 2.2
running on UNIX, and only when the Apache runtime library underlying Apache
has been compiled with support for threading.

Python 2.X is required with a minimum of Python 2.3. The Python
installation being used must have been compiled with support for threading.

The original WSGI specification `PEP 333`_ only supports Python 2.X. There
was support added in mod_wsgi version 3.0 for Python 3.X which is based on
guesses as to what the WSGI specification would look like for Python 3.X.
The new WSGI specification `PEP 3333`_ has finally now been accepted and
although some tweaks need to be made to mod_wsgi to make it more strict, if
you write your Python 3 WSGI application according to PEP 3333, it will
work perfectly fine on mod_wsgi. If you wish to experiment with Python 3.X,
you will need to use Python 3.1 or later. To use Python 3.2 however, you
will currently need to use the in development version of mod_wsgi 4.0
available from the `source code repository`_.

.. _source code repository: http://code.google.com/p/modwsgi/source/checkout

.. _WSGI: http://www.python.org/dev/peps/pep-0333/
.. _PEP 333: http://www.python.org/dev/peps/pep-0333/
.. _PEP 3333: http://www.python.org/dev/peps/pep-3333/
