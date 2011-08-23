

========================
Quick Installation Guide
========================

This document describes the steps for installing mod_wsgi on a UNIX system
from the original source code.

Getting Further Help
--------------------

If you have problems following the instructions in this document, or
something doesn't work and the documentation doesn't help, post your
questions to the mod_wsgi mailing list hosted on Google Groups at:

  http://groups.google.com/group/modwsgi

Apache Requirements
-------------------

Apache 1.3, 2.0 or 2.2 can be used.

For Apache 1.3 the core Apache modules must be dynamically loaded. If the
core modules are statically linked then some features of mod_wsgi will not
work correctly.

For Apache 2.0 and 2.2, either the single threaded 'prefork' or
multithreaded 'worker' Apache MPMs can be used.

To be able to make use of daemon mode of mod_wsgi, either Apache 2.0 or 2.2
is required and the corresponding Apache runtime (APR) libraries must have
been compiled with support for threading.

On Linux systems, if Apache has been installed from a package repository,
you must have installed the corresponding Apache "dev" package as well.

For most Linux distributions, the "dev" package for Apache 2.X is
"apache2-dev" where the corresponding Apache package was "apache2". Some
systems however distinguish the "dev" package based on which MPM is used by
Apache. As such, it may also be called "apache2-worker-dev" or
"apache2-prefork-dev". If using Apache 2.X, do not mix things up and install
"apache-dev" by mistake, which is the "dev" package for Apache 1.3 called
just "apache".

Python Requirements
-------------------

And Python 2.X version from Python 2.3 onwards can be used. Python 3.0 and
later will only be able be used with mod_wsgi 3.0 when released.

The version of Python being used must have been compiled with support for
threading.

On Linux systems, if Python has been installed from a package repository,
you must have installed the corresponding Python "dev" package as well.

Python should preferably be available as a shared library. If this is not
the case then base runtime memory usage of mod_wsgi will be greater and
conflicts with mod_python can occur causing Apache to crash if both Apache
modules are loaded at the same time.

Unpacking The Source Code
-------------------------

Source code tar balls can be obtained from:

  http://code.google.com/p/modwsgi/downloads/list

After having downloaded the tar ball for the version you want to use,
unpack it with the command:

::

    tar xvfz mod_wsgi-X.Y.tar.gz


Replace 'X.Y' with the actual version number for that being used.

Configuring The Source Code
---------------------------

To setup the package ready for building run the "configure" script from
within the source code directory.

::

    ./configure


The configure script will attempt to identify the Apache installation to
use by searching in various standard locations for the Apache build tools
included with your distribution called "apxs2" or "apxs". If not found in
any of these standard locations, your PATH will be searched.

Which Python installation to use will be determined by looking for the
"python" executable in your PATH.

If these programs are not in a standard location, they cannot be found in
your PATH, or you wish to use alternate versions to those found, the
"--with-apxs" and "--with-python" options can be used in conjunction with
the "configure" script.

::

    ./configure --with-apxs=/usr/local/apache/bin/apxs \
      --with-python=/usr/local/bin/python


On some Linux distributions, such as SUSE and CentOS, it will be necessary
to use the "--with-apxs" option and specify either "/usr/sbin/apxs2-worker"
or "/usr/sbin/apxs2-prefork". This is necessary as the Linux distribtions
allow installation of "dev" packages for both Apache MPM variants at the
same time, whereas other Linux distributions do not.

If you have multiple versions of Python installed and you are not using
that which is the default, you may have to organise that the PATH inherited
by the Apache application when run will result in Apache finding the
alternate version. Alternatively, the WSGIPythonHome directive should
be used to specify the exact location of the Python installation
corresponding to the version of Python compiled against. If this is not
done, the version of Python running within Apache may attempt to use the
Python modules from the wrong version of Python.

Building The Source Code
------------------------

Once the package has been configured, it can be built by running:

::

    make


If the mod_wsgi source code does not build successfully, see:

  * [InstallationIssues Installation Issues]

Documentation is also provided for installing mod_wsgi on a range of
different operating systems. These following documents may also list issues
specific to those plaforms:

  * [InstallationOnLinux Installation On Linux]
  * [InstallationOnMacOSX Installation On MacOS X]
  * [InstallationOnSolaris Installation On Solaris]
  * [InstallationOnFreeBSD Installation On FreeBSD]

If successful, the only product of the build process that needs to be
installed is the Apache module itself. There are no separate Python code
files as everything is done within C code compiled into the Apache module.

To install the Apache module into the standard location for Apache modules
as dictated by Apache for your installation, run:

::

    make install


Installation should be done as the 'root' user or 'sudo' command if
appropriate.

If you want to install the Apache module in a non standard location
dictated by how your operating system distribution structures the
configuration files and modules for Apache, you will need to copy the file
manually into place.

If installing the Apache module by hand, the file is called 'mod_wsgi.so'.
If you are using Apache 1.3 the compiled Apache module can be found in the
source directory. If you are using Apache 2.X the compiled Apache module
can be found in the ".libs" subdirectory. The name of the file should be
kept the same when copied into its appropriate location.

Loading Module Into Apache
--------------------------

Once the Apache module has been installed into your Apache installation's
module directory, it is still necessary to configure Apache to actually
load the module.

Exactly how this is done and in which of the main Apache configuration
files it should be placed, is dependent on which version of Apache you are
using and may also be influenced by how your operating system's Apache
distribution has organised the Apache configuration files. You may
therefore need to check with any documentation for your operating system to
see in what way the procedure may need to be modified.

In the simplest case, all that is required is to add a line of the form:

::

    LoadModule wsgi_module modules/mod_wsgi.so


into the main Apache "httpd.conf" configuration file at the same point that
other Apache modules are being loaded. The last option to the directive
should either be an absolute path to where the mod_wsgi module file is
located, or a path expressed relative to the root of your Apache
installation. If you used "make" to install the package, see where it
copied the file to work out what to set this value to.

With Apache 1.3, it is also necessary to add a line of the form:

::

    AddModule mod_wsgi.c


For Apache 1.3, the !LoadModule and !AddModule lines related to mod_wsgi
must appear prior to those for the Apache code module called mod_alias.

Restart Apache Web Server
-------------------------

Having adding the required directives you should perform a restart of
Apache to check everything is okay. If you are using an unmodified Apache
distribution from the Apache Software Foundation, a restart is performed
using the 'apachectl' command.

::

    apachectl restart


If you see any sort of problem, or if you are upgrading from an older
version of mod_wsgi, it is recommended you actually stop and the start
Apache instead.

::

    apachectl stop
    apachectl start


Note that on many Linux distributions where Apache is prepackaged, the
Apache software has been modified and as a result the 'apachectl' command
may not work properly or the command may not be present. On these systems,
you will need to use whatever is the sanctioned method for restarting
system services.

This may be via an 'init.d' script:

::

    /etc/init.d/httpd stop
    /etc/init.d/httpd start


or via some special service maintenance script.

On Debian derived distributions, restarting Apache is usually done via the
'invoke-rc.d' command. For an Apache 1.3 installation it would be executed
as:

::

    invoke-rc.d apache stop
    invoke-rc.d apache start


For Apache 2.X, the service name would instead be called 'apache2'.

On !RedHat derived distributions, restarting Apache is usually done via the
'service' command:

::

    service httpd stop
    service httpd start


Where 'apachectl' does still exist, it may actually be called 'apachectl2'
if the system allows for both Apache 1.3 and Apache 2.X to be installed at
the same time.

In nearly all cases the scripts used to restart Apache will need to be run
as the 'root' user or via 'sudo'.

In general, for any system where you are using a prepackaged version of
Apache, it is wise to always check the documentation for that package or
system to determine the correct way to restart the Apache service. This is
because they often use a wrapper around 'apachectl', or replace it, with a
script which performs additional actions.

If all is okay, you should see a line of the form:

::

    Apache/2.2.2 (Unix) mod_wsgi/1.0 Python/2.3 configured


in the Apache error log file.

Cleaning Up After Build
-----------------------

To cleanup after installation, run:

::

    make clean


If you need to build the module for a different version of Apache, you
should run:

::

    make distclean


and then rerun "configure" against the alternate version of Apache before
attempting to run "make" again.

Debugging Any Problems
----------------------

If you have any problems trying to install mod_wsgi, see:

  * [InstallationIssues Installation Issues]
  * [ConfigurationIssues Configuration Issues]

Configuring An Application
--------------------------

For details on how to configure mod_wsgi to run a basic WSGI application,
and thus verify that your mod_wsgi configurationn is working, see:

  * [QuickConfigurationGuide Quick Configuration Guide]

For more in depth information on configuring mod_wsgi see:

  * [ConfigurationGuidelines Configuration Guidelines]
  * [ConfigurationDirectives Configuration Directives]

Documentation is also provided for using mod_wsgi with some of the common
Python web frameworks and applications:

  * [IntegrationWithCherryPy Integration With CherryPy]
  * [IntegrationWithDjango Integration With Django]
  * [IntegrationWithMoinMoin Integration With MoinMoin]
  * [IntegrationWithPylons Integration With Pylons]
  * [IntegrationWithRepozeBFG Integration With Repoze BFG]
  * [IntegrationWithTrac Integration With Trac]
  * [IntegrationWithTurboGears Integration With TurboGears]
  * [IntegrationWithWebPy Integration With web.py]
  * [IntegrationWithWeb2Py Integration With web2py]
  * [IntegrationWithWerkzeug Integration With Werkzeug]
