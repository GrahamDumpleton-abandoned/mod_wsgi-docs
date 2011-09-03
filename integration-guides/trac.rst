=====================
Integration With Trac
=====================

Note: Requires Trac 0.10 or later.

Note: This is not intended as a basic tutorial on how to setup mod_wsgi.
It is recommended you first read more introductory material for mod_wsgi.
Start by reading through various documents linked off
:doc:`../installation-guides/index`.

The `Trac <http://trac.edgewall.org/>`_ application provides the
``trac.web.main.dispatch_request()`` function for running Trac as a WSGI
application. A script file for a Trac application which is compatible with
mod_wsgi would be constructed as follows::

    import os
    os.environ['TRAC_ENV'] = '/usr/local/trac/site-1'

    import trac.web.main

    application = trac.web.main.dispatch_request

The ``TRAC_ENV`` environment variable should be set as appropriate for
Trac to indicate where the Trac site instance has been installed in the
filesystem.

If using the embedded application mode of mod_wsgi, because an application
is run as the user that Apache runs as, if Python eggs are being used for
Trac plugins it may not have the ability to create a cache directory in
the default location. Therefore, it may be necessary to set the environment
variable ``PYTHON_EGG_CACHE`` at the start of the script file to an
appropriate directory where the Apache user has write permission and into
which it can unpack egg files.

Because portable WSGI applications should never write to 'sys.stdout'
directly or indirectly using 'print', by default mod_wsgi will restrict use
of 'sys.stdout'. Some Trac plugins however are known to use 'print' to
output debug information when they should not do so if they want to be able
to work on all WSGI platforms. As such, as well as defining a directory for
the Python egg cache, it may be necessary to override the mod_wsgi
restriction on using 'sys.stdout' by mapping it to 'sys.stderr' instead.

The script file may therefore need to be::

    import sys
    sys.stdout = sys.stderr

    import os
    os.environ['TRAC_ENV'] = '/usr/local/trac/site-1'
    os.environ['PYTHON_EGG_CACHE'] = '/usr/local/trac/site-1/eggs'

    import trac.web.main

    application = trac.web.main.dispatch_request

In either case, an example of how Apache could be configured for a single
site would be::

    WSGIScriptAlias /trac /usr/local/trac/site-1/apache/trac.wsgi

    <Directory /usr/local/trac/site-1/apache>
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

This would result in the Trac site being accessible as '/trac'.

The configuration shown presumes that an 'apache' subdirectory has been
created within the Trac site instance and the script file stored there
under the name 'trac.wsgi'. A separate directory is used, as it is
necessary to indicate to Apache that it is allowed access to files in that
directory, something you wouldn't want to do for all your Trac data.

Do note that some versions of the Subversion Python bindings apparently
have problems when being used from within secondary Python sub interpreters
rather than the main Python interpreter. The result of this will be strange
Python exceptions or the Apache child processes could even crash.

To avoid such problems, the Trac application should be forced to run within
the main Python interpreter. This can be done using the WSGIApplicationGroup
directive with the value '%{GLOBAL}' as shown.

Because of the need to force Trac to run in the main Python interpreter,
you can only run one Trac instance at a time if using the environment
variable approach to configuring Trac. If needing to run multiple Trac
instances, you need to use Trac's support for running multiple sites, use
daemon mode of mod_wsgi and delegate each Trac instance to a separate
daemon process group, or use the WSGI environment variable approach to
configuring Trac.

If using Apache based authentication for Trac users, configuration similar
to the following would also be required::

    <Location /trac/login>
    AuthType Basic
    AuthName "Trac Site 1"
    AuthUserFile /usr/local/trac/site-1/.htpasswd
    Require valid-user
    </Location>

If you are using a single Trac installation to host multiple projects, you
could also set ``TRAC_ENV_PARENT_DIR`` instead of ``TRAC_ENV`` and
refer to the parent filesystem directory where the sites are kept. The
script file would then be::

    import sys
    sys.stdout = sys.stderr

    import os
    os.environ['TRAC_ENV_PARENT_DIR'] = '/usr/local/trac/sites'
    os.environ['PYTHON_EGG_CACHE'] = '/usr/local/trac/eggs'

    import trac.web.main

    application = trac.web.main.dispatch_request

The Apache configuration for the case of hosting multiple sites within the
one Trac instance would be::

    WSGIScriptAlias /trac /usr/local/trac/apache/trac.wsgi

    <Directory /usr/local/trac/apache>
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

The benefit of running the multiple Trac instances in the same Python
interpreter is that any Python modules are only loaded once for all sites,
rather than each interpreter holding its own copy. This will result in less
memory being used.

The configuration shown presumes that an 'apache' subdirectory has been
created outside the directory holding all the Trac sites. Similarly with
the Python eggs directory.

When hosting multiple sites in this way, Trac will automatically create you
an index page for the parent URL of all the Trac sites with links to the
individual sites. This will be accessible as '/trac', with the different
Trac sites appearing as subdirectories of '/trac'.

If you wish to customise this index page, you should set the
``TRAC_ENV_INDEX_TEMPLATE`` environment variable to be the location of
the template to use. For further details on customising this index page see
Trac `interface customisation <http://trac.edgewall.org/wiki/TracInterfaceCustomization>`_ page.

Whether one site is being hosted or many sites, they need not be mounted as
a sub directory of the URL namespace. To host a single site on the root of
the web server the following could also be used::

    WSGIScriptAlias / /usr/local/trac/site-1/apache/trac.wsgi

    <Directory /usr/local/trac/site-1/apache>
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

Although Trac can be run using the embedded application mode of mod_wsgi,
with the Trac parent directory support allowing for the hosting of multiple
sites within the one interpreter, it is possibly preferable that it be run
in conjunction with daemon process mode.

The benefits of using daemon process mode in this case are that each Trac
site can be run in a distinct process. This will allow Trac sites to safely
run a different version of the Trac software or use a different version of
the Subversion Python bindings. Each Trac instance may also use different
sets of plugins.

Normally using different versions of any Python software like this in the
same process, even in different Python sub interpreters, can be a problem.
This is because Python only loads a C extension module once for the entire
process. Thus if any of the packages where different versions were being
used comprised C extension modules, such as the Subversion Python bindings,
Python would use whichever version of the C extension module was loaded
first for all sub interpreters. As a result, any Python code which expected
a different version to have been loaded would most likely fail.

A final benefit of using daemon process mode, is that it would be possible
to run the Trac instances as a user other than that which the Apache
processes would normally run as.

A configuration for running two distinct Trac instances, each using a
single daemon process run as the user 'trac' would be::

    WSGIDaemonProcess site-1 user=trac group=trac threads=25
    WSGIScriptAlias /site-1 /usr/local/trac/site-1/apache/trac.wsgi

    <Directory /usr/local/trac/site-1/apache>
    WSGIProcessGroup site-1
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

    WSGIDaemonProcess site-2 user=trac group=trac threads=25
    WSGIScriptAlias /site-2 /usr/local/trac/site-2/apache/trac.wsgi

    <Directory /usr/local/trac/site-2/apache>
    WSGIProcessGroup site-2
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

In addition to configuring Trac using environment variables as shown above,
Trac may also be configured by variables passed through the WSGI
application environment. This may be done in a WSGI application wrapper, or
by using the SetEnv directive within the Apache configuration files. The
names of the WSGI application environment variables which are honoured and
the equivalent Python environment variables are as follows:

:trac.env_path: TRAC_ENV
:trac.env_parent_dir: TRAC_ENV_PARENT_DIR
:trac.env_index_template: TRAC_ENV_INDEX_TEMPLATE
:trac.template_vars: TRAC_TEMPLATE_VARS
:trac.locale:

If being done using a WSGI application wrapper as described, the WSGI
script file would be written as::

    import trac.web.main

    _application = trac.web.main.dispatch_request

    def application(environ, start_response):
      environ['trac.env_path'] = '/usr/local/trac/site-1'
      return _application(environ, start_response)

An Apache configuration, using the SetEnv directives for configuring
Trac, might alternatively be as follows::

    WSGIDaemonProcess site-1 user=trac group=trac threads=25
    WSGIScriptAlias /site-1 /usr/local/trac/site-1/apache/trac.wsgi

    <Directory /usr/local/trac/site-1/apache>
    WSGIProcessGroup site-1
    WSGIApplicationGroup %{GLOBAL}
    SetEnv trac.env_path /usr/local/trac/site-1
    Order deny,allow
    Allow from all
    </Directory>

    WSGIDaemonProcess site-2 user=trac group=trac threads=25
    WSGIScriptAlias /site-2 /usr/local/trac/site-2/apache/trac.wsgi

    <Directory /usr/local/trac/site-2/apache>
    WSGIProcessGroup site-2
    WSGIApplicationGroup %{GLOBAL}
    SetEnv trac.env_path /usr/local/trac/site-2
    Order deny,allow
    Allow from all
    </Directory>

With this configuration, there is no need to set environment variables
within the script file and the minimal WSGI script file show below could
be used::

    import trac.web.main

    application = trac.web.main.dispatch_request

If wishing to host multiple sites within the one daemon process group,
instead of using the ``TRAC_ENV_PARENT_DIR`` process environment
variable, one can use the WSGI environment variable 'trac.env_parent_dir'::

    WSGIDaemonProcess sites user=trac group=trac processes=3 threads=25
    WSGIScriptAlias /trac /usr/local/trac/apache/trac.wsgi

    <Directory /usr/local/trac/apache>
    WSGIProcessGroup sites
    WSGIApplicationGroup %{GLOBAL}
    SetEnv trac.env_parent_dir /usr/local/trac/sites
    Order deny,allow
    Allow from all
    </Directory>

If wishing to automate the configuration so as to make it easier to manage
a large number of Trac sites, where each runs in a distinct daemon process
and as a different user, the following configuration may be more
appropriate::

    WSGIDaemonProcess site-1 user=user-1 group=user-1 threads=25
    WSGIDaemonProcess site-2 user=user-2 group=user-2 threads=25
    WSGIDaemonProcess site-3 user=user-3 group=user-3 threads=25
    WSGIDaemonProcess site-4 user=user-4 group=user-4 threads=25
    WSGIDaemonProcess site-5 user=user-5 group=user-5 threads=25
    WSGIDaemonProcess site-6 user=user-6 group=user-6 threads=25

    RewriteEngine On
    RewriteCond %{REQUEST_URI} ^/trac/([^/]+)
    RewriteRule . - [E=trac.process_group:%1,\
    E=trac.env_path:/usr/local/trac/sites/%1]

    WSGIScriptAliasMatch ^/trac/([^/]+) /usr/local/trac/apache/trac.wsgi

    <Directory /usr/local/trac/apache>
    WSGIProcessGroup %{ENV:trac.process_group}
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

In order to add a new Trac site, a new Trac instance directory would be
created under the parent directory '/usr/local/trac/sites', a new
WSGIDaemonProcess entry added to the Apache configuration file and Apache
restarted. Changes are still required to the Apache configuration so as to
add the directive related to the new daemon process and define the user
and group of that process, but at least the changes have been limited
to one line.

If not specifically needing the ability to delegate different instances of
Trac to different daemon processes so as to run as different users, or in
order to allow different versions of Trac or plugins to be used, one can
still use daemon processes purely for the benefit derived from not having
Trac running in the main Apache child processes. In particular, delegating
Trac to a daemon process means that the Apache child processes handling
requests for static files or dynamic pages implemented by other languages
such as PHP, will not be bloated out in size by the presence of Trac.

Where the the Trac mechanism for supporting multiple sites within the one
interpreter is not flexible enough, then dynamically setting the WSGI
environment variable 'trac.env_path' can also be done using a rewrite
rule based on some part of the URL. Except for there being no automatically
generated index page, an equivalent to Trac's own support for multiple
sites would be as follows::

    WSGIDaemonProcess sites processes=3 threads=25 maximum-requests=1000

    RewriteEngine On

    RewriteCond %{REQUEST_URI} ^/trac/([^/]+)
    RewriteCond /usr/local/trac/sites/%1/conf/trac.ini !-f
    RewriteRule . - [F]

    RewriteCond %{REQUEST_URI} ^/trac/([^/]+)
    RewriteRule . - [E=trac.env_path:/usr/local/trac/sites/%1]

    WSGIScriptAliasMatch ^/trac/([^/]+) /usr/local/trac/apache/trac.wsgi

    <Directory /usr/local/trac/apache>
    WSGIProcessGroup sites
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
    </Directory>

This configuration could be adapted as necessary where for example all Trac
sites are not stored under the one directory but spread across the file
system in different directories. This could be done through the rewrite
rules directly or using a rewrite map file.

Using rewrite rules in this way should only be done where the Trac
mechanism for hosting multiple sites within the one interpreter is not
sufficient. Normally Trac's own mechanism should be used.

To avoid any possibility of process memory use growing over time due to
unknown memory leaks, one can also define a maximum number of requests
before an individual daemon process is shutdown and restarted. Because of
the possibility that a Trac process may be slow to shutdown, it is
recommended though that when setting a maximum for the number of requests,
that the number of processes in the daemon process group be set to 2 or
more. This is so that when one process is being shutdown and restarted,
that the chances are that the other is still accepting requests at that
time and there will be no perceived pause in handling of requests.

The maxmimum number of requests allowed before a daemon process is shutdown
and restarted would need to be determined to a degree through trial and
error. One should avoid setting it to to small a value however, as this
will result in daemon process restarts being very close together when the
site is under load.

For other suggestions regarding how to configure mod_wsgi specifically
for Trac, also check out the Trac page at:

  http://trac.edgewall.org/wiki/TracModWSGI
