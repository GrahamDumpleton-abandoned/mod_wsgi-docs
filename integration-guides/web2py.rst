=======================
Integration With web2py
=======================

For information about how to use webp2y in conjunction with mod_wsgi, see
section 'Setup mod_wsgi on Linux' (about page 301 of whole document) of
the web2py book at:

  http://www.scribd.com/doc/19211452/Web2py-Manual

Downloadable version of the web2py book also available from:

  http://www.lulu.com/content/e-book/web2py/4968879

Do note though, that the example configuration in the book has failed to
use a line continuation character when wrapping Apache configuration lines.
You should ensure that WSGIDaemonProcess and AliasMatch directive options
are all on the same line as the directive, or end the first line with
a backslash to continue the line.

Only use the configuration example from the second edition of the book. Do
not use those from the first edition as it had many mistakes in it which have
been detailed at:

  http://blog.dscpl.com.au/2009/08/problems-with-example-web2py.html

  http://blog.dscpl.com.au/2009/08/more-on-those-problems-with-example.html

If you require assistance with getting web2py working, then try the
'web2py' mailing list or '#web2py' channel on IRC. The Google Groups
interface for the mailing list is at:

  http://groups.google.com/group/web2py
