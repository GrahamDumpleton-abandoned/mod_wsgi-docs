=====================
Installation On Linux
=====================

If using a Linux system, mod_wsgi can be installed direct from source code.

For descriptions of general problems that may be encountered during
installation on Linux, see the documentation on
:doc:`InstallationIssues`.

If however you prefer to use packages specific to your Linux distribution,
details of known packages are listed given below.

Debian Packages
---------------

Details on Debian packages can be found at:

  http://packages.debian.org/unstable/python/libapache2-mod-wsgi

Thanks to Bernd Zeimetz for preparing and putting together this distribution.

RHEL/Centos Packages
--------------------

The IUS Community Project publishes RPMs for both Python 2.6 and Python
3.1, as well as the compatible mod_wsgi packages.

  http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/SRPMS/repoview/mod_wsgi-python26.html
  http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/SRPMS/repoview/mod_wsgi-python31.html

The main page for the IUS community is:

  http://iuscommunity.org/packages/

Another source of more up to date, but unofficial, binary packages for RPM
based systems, see:

  http://codepoint.net/attachments/mod_wsgi/

These rely on using the standard version of Python installed on those systems.

Fedora Packages
---------------

Official Fedora packages seem to be hopelessly out of date and are actually
for a version of mod_wsgi which isn't recommended be used anymore.

Only known URL is:

  http://download.fedora.redhat.com/pub/epel/5/i386/repoview/mod_wsgi.html

For an alternate set of more up to date, but unofficial, binary packages
for RPM based systems, see:

  http://codepoint.net/attachments/mod_wsgi/

These rely on using the standard version of Python installed on those systems.

Arch Linux Packages
-------------------

Details on Arch Linux packages can be found at:

  http://aur.archlinux.org/packages.php?ID=13394

Thanks to Nicolas Steinmetz for preparing and putting together this
distribution.

SUSE Linux Packages
-------------------

Details on SUSE Linux packages can be found at:

  http://software.opensuse.org/search?q=mod_wsgi

Thanks to Peter Poeml for preparing and putting together this distribution.

Restarting Apache Service
-------------------------

When using a prepackaged Apache on a Linux system, they will have generally
integrated starting and stopping of Apache into the operating system
service management features. When this is the case, the 'apachectl' script
may not work as originally intended by the Apache authors and it is instead
necessary to always use the operating system specific mechanism to start,
stop or restart Apache.

An example of an error which may occur when trying to restart Apache using
'apachectl' on such a system is::

    httpd (pid 22361?) not running
    (98)Address already in use: make_sock: could not bind to address 0.0.0.0:80
    no listening sockets available, shutting down
    Unable to open logs

Because the exact mechanism used to manage services can differ between
Linux operating system variants, you should consult the documentation for
the prepackage version of Apache, or that for the operating system itself.

One approach used requires that the 'init.d' script be used directly::

    /etc/init.d/apache2 stop
    /etc/init.d/apache2 start

Another is to use an intermediary management script, which in turns executes
the appropriate 'init.d' script::

    invoke-rc.d apache2 reload
