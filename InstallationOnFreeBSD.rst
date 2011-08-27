=======================
Installation On FreeBSD
=======================

If using a FreeBSD system, mod_wsgi can be compiled from source code by
following standard installation instructions. Alternatively you can install
from FreeBSD ports as detailed below.

For descriptions of general problems that may be encountered during
installation on FreeBSD, see the documentation on
:doc:`InstallationIssues`.

Installation From FreeBSD Ports
-------------------------------

You will first want to make sure to install Apache before installing
mod_wsgi because FreeBSD ports will just install the minimum supported
version otherwise. Choose the version of Apache (for this example we use
Apache 2.2).

Read '/usr/ports/www/apache22/Makefile.doc' for information about options.
If you want to use the worker MPM you will need to add::

    WITH_MPM=worker

to '/etc/make.conf'.

To install Apache::

    # cd /usr/ports/www/apache22
    # make config

Make sure 'THREADS' is selected and review other options before selecting
OK::

    # make
    # make install

To install mod_wsgi itself, you can then go::

    # cd /usr/ports/www/mod_wsgi3
    # make
    # make install

If you find that mod_wsgi daemon mode is not available, make sure APR isn't
installed without threads. Its package name will include "nothr" if threads
are disabled::

    # pkg_info -x ^apr- | head -n 1
    Information for apr-nothr-1.4.2.1.3.9_1:

In this case you will need to rebuild everything. That is, the APR library
as well as Apache. Make sure 'WITHOUT_THREADS' isn't defined in
'/etc/make.conf' and then run::

    # cd /usr/ports/devel/apr1
    # make config

Then make sure 'THREADS' is selected and review other options before
selecting OK::

    # make
    # make deinstall
    # make reinstall

Then do the same with Apache::

    # cd /usr/ports/devel/apache22
    # make config

Again make sure THREADS is selected and review other options before
selecting OK::

    # make
    # make deinstall
    # make reinstall

You can then go onto install mod_wsgi once more.

Daemon Mode Not Available
-------------------------

Even though one might be using Apache 2.X on FreeBSD, one might encounter
when starting Apache, the error::

    Syntax error on line 7 of /usr/local/etc/apache22/Includes/test.conf:
      Invalid command 'WSGIDaemonProcess', perhaps misspelled or defined by
      a module not included in the server configuration

Presuming that mod_wsgi is being correctly loaded into Apache, this would
generally indicate that daemon mode support has not actually been compiled
into mod_wsgi.

When using Apache 2.X, this can occur where the underlying Apache Runtime
Libraries (APR) haven't been compiled so as to include support for
threading.

On some FreeBSD systems, the default seems to be that Apache prefork MPM is
used, and since that doesn't require threading, then threading support isn't
built into the separate APR libraries either.

One can validate whether the APR libraries have threading support enabled,
by finding where the APR header files are installed and looking at the
include file "apr.h". If threading is enabled, you should find::

    #define APR_HAS_THREADS           1

If instead the definition of APR_HAS_THREADS is commented out, then threading
support would be disabled. Although it shouldn't ever be the case, that
preprocessor macro could technically be set to 0 if threading is disabled,
but usually the autoconf system doesn't do that and comments out the line
instead.

The solution would be to reinstall the APR libraries, Apache and mod_wsgi
but configure the APR libraries with support for threading.

If the APR libraries within Apache are being used, rather than a separate
APR installation, this can be done by explicitly supplying the option
'--enable-threads' to the 'configure' script when building Apache.

If the APR libraries are separate, then they instead would need to be
rebuilt with threading enabled and then Apache and mod_wsgi rebuilt.
Instructions for doing this for FreeBSD ports as explained above.

Undefined Thread Functions
--------------------------

The version of Apache on older versions of FreeBSD is not compiled with
support for multithreading, or even linked with any thread libraries, but
Python itself requires the threading libraries. The result is that when
starting up Apache with mod_wsgi, an error similar to the following can
occur::

    Syntax error on line 37 of /usr/local/apache2/conf/httpd.conf: \
     Cannot load /usr/local/apache2/modules/mod_wsgi.so into server: \
     /usr/local/apache2/modules/mod_wsgi.so: Undefined symbol \
     "pthread_attr_init"

The solution is to force Apache to preload the reentrant version of the C
runtime library which contains the POSIX thread library functions. This can
be done by modifying the 'envvars' script, if it exists and is used,
contained in the same directory as where the Apache 'httpd' binary is
installed, or the Apache startup script, and add the lines::

    LD_PRELOAD=/usr/lib/libc_r.so
    export LD_PRELOAD

On more recent versions of FreeBSD, especially where Apache 2.X is being
used, the above should not be required. In fact, having the above definition
present will actually cause Apache to crash when loading mod_wsgi.
