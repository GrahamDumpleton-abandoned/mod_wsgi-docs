

============================
Integration With !TurboGears
============================

_Note: Requires !TurboGears 1.X. Instructions may not be applicable
to !TurboGears 2.0. For !TurboGears 2.0, because it is based on Pylons
you may actually need to refer to
[IntegrationWithPylons Integration With Pylons]._

_Note: This is not intended as a basic tutorial on how to setup mod_wsgi.
It is recommended you first read more introductory material for mod_wsgi.
Start by reading through various documents linked off
[InstallationInstructions Installation Instructions]._

The [http://www.turbogears.org/ TurboGears] framework is built on top of
!CherryPy and inherits its ability to be used on top of a WSGI server from
!CherryPy. As !TurboGears doesn't use the latest version of !CherryPy, the
steps required to startup !CherryPy are however slightly different to that
for !CherryPy 3.0. Thus a script file for a !TurboGears application which
is compatible with mod_wsgi would be constructed as follows:

::

    import sys
    sys.path.append('/usr/local/turbogears/mysite')
    sys.stdout = sys.stderr
    
    import os
    os.environ['PYTHON_EGG_CACHE'] = '/usr/local/turbogears/python-eggs'
    
    import atexit
    import cherrypy
    import cherrypy._cpwsgi
    import turbogears
    
    turbogears.update_config(configfile="dev.cfg", modulename="mysite.config")
    turbogears.config.update({'global': {'server.environment': 'production'}})
    turbogears.config.update({'global': {'autoreload.on': False}})
    turbogears.config.update({'global': {'server.log_to_screen': False}})
    
    import mysite.controllers
    
    cherrypy.root = mysite.controllers.Root()
    
    if cherrypy.server.state == 0:
        atexit.register(cherrypy.server.stop)
        cherrypy.server.start(init_only=True, server_class=None)
    
    application = cherrypy._cpwsgi.wsgiApp


The directory added to ``sys.path`` would be the directory for the
!TurboGears site created by running:

::

    tg-admin quickstart


The 'configfile' argument supplied to ``turbogears.update_config()``
should be replaced with appropriate value for your installation. This
would generally need to be an absolute path.

Although !CherryPy provides a WSGI application object, it is currently
still necessary as shown above to startup the internal !CherryPy engine and
ensure that it is subsequently shutdown on process shutdown.

It is necessary to ensure that the !CherryPy engine is stopped on process
shutdown, otherwise the threads that the !CherryPy engine uses will prevent
the Apache child process from shutting down cleanly and instead it will
hang. This will have the result that the Apache parent process will have to
forcibly kill off the child processes.

Because an application is run as the user that Apache runs as, if Python
eggs are being used and there is a need for eggs to be unpacked on the fly,
it may not have the ability to create a cache directory in the default
location. Therefore, it may be necessary to set the environment variable
``PYTHON_EGG_CACHE`` at the start of the script file to an appropriate
directory where the Apache user has write permission and into which it can
unpack egg files.

A suitable Apache configuration for !TurboGears would be as follows:

::

    WSGIScriptAlias / /usr/local/turbogears/mysite/apache/turbogears.wsgi
    
    <Directory /usr/local/turbogears/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>


The configuration shown presumes that an 'apache' subdirectory has been
created within the !TurboGears site instance and the script file stored
there under the name 'turbogears.wsgi'.

If using !TurboGears 1.0 and you need to host the !TurboGears application at
a mount point other than the root of the web server, the mount point will
have to be defined in the script file as the 'server.webpath' configuration
option. A wrapper for the !CherryPy WSGI application entry point will also
need to be used to explicitly set the 'SCRIPT_NAME' variable to an empty
string. Both these changes are required as !TurboGears 1.0 is not a truly
WSGI compliant application and does not honour the 'SCRIPT_NAME' variable
passed in the WSGI application environment.

::

    import sys
    sys.path.append('/usr/local/turbogears/mysite')
    sys.stdout = sys.stderr
    
    import os
    os.environ['PYTHON_EGG_CACHE'] = '/usr/local/turbogears/python-eggs'
    
    import atexit
    import cherrypy
    import cherrypy._cpwsgi
    import turbogears
    
    turbogears.update_config(configfile="dev.cfg", modulename="mysite.config")
    turbogears.config.update({'global': {'server.environment': 'production'}})
    turbogears.config.update({'global': {'autoreload.on': False}})
    turbogears.config.update({'global': {'server.log_to_screen': False}})
    turbogears.config.update({'global': {'server.webpath': '/mysite'}})
    
    import mysite.controllers
    
    cherrypy.root = mysite.controllers.Root()
    
    if cherrypy.server.state == 0:
        atexit.register(cherrypy.server.stop)
        cherrypy.server.start(init_only=True, server_class=None)
    
    def application(environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return cherrypy._cpwsgi.wsgiApp(environ, start_response)


The corresponding Apache configuration for the !TurboGears application
being mounted as '/mysite' would be:

::

    WSGIScriptAlias /mysite /usr/local/turbogears/mysite/apache/turbogears.wsgi
    
    <Directory /usr/local/turbogears/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>


To ensure that URLs produced by your application will always be correct
whether the application is mounted at the root of the web server or a sub
URL, you should ensure you use the appropriate
[http://docs.turbogears.org/1.0/GettingStarted/URLs url functions]. These
will ensure the correct application root always appears in generated URLs.

The above changes to handle mounting a !TurboGears instance at a URL other
than the root URL should not be required for !TurboGears 1.1 as it has been
updated to automatically set 'server.webpath' to the value of 'SCRIPT_NAME'
if 'server.webpath' is not otherwise set.

Note that you may not be able to use the 'Interpreter' option for
the WSGIReloadMechanism directive when using !TurboGears. This is because
the !PyProtocols package that !TurboGears in some way relies upon is not
able to cope with sub interpreters being destroyed and a new sub
interpreter being created, from which the !PyProtocols package is once
again being imported.

The result of attempting to use the 'Interpreter' option will be
unpredictable, but can range from the Apache child process crashing to
random Python exceptions. The actual problems seem to stem from the use of
Pyrex generated C code in !PyProtocols. At this stage it is not known
whether the problems are with how !PyProtocols uses Pyrex, or whether Pyrex
itself doesn't generate code which is safe to use with multiple sub
interpreters.

Also note that the !CherryPy engine appears to default to logging to
``sys.stdout`` when a portable WSGI component application should not do
that. To catch such portability problems mod_wsgi restricts use of
``sys.stdout``. To avoid the restriction, ``sys.stdout`` is mapped to
``sys.stderr`` in the script. Instead of doing the mapping in the script
the ``WSGIRestrictStdout`` directive could also be set to ``Off``.

Although the above configuration will allow !TurboGears to be run, there
have been question marks in the past over whether !TurboGears will work
properly in a multiprocess web server. Any problems seem to resolve around
database caching performed by the application instance in each process not
being in sync.

The latest analysis on this suggests that if SQLObject is being used in the
database layer then you may encounter problems. If however using a more
recent version of !TurboGears and are instead using SQLAlchemy in place of
SQLObject, then you will not be affected. This problem is also understood
to have been addressed for SQLObject in !TurboGears 1.1.

If unsure as to whether you might be affected by this issue, it may be
preferable to run !TurboGears in conjunction with daemon mode of mod_wsgi
with a single process.

::

    WSGIDaemonProcess site-1 threads=25
    WSGIProcessGroup site-1
    
    WSGIScriptAlias / /usr/local/turbogears/mysite/apache/turbogears.wsgi
    
    <Directory /usr/local/turbogears/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>


Daemon mode is also preferable for the reason that !TurboGears applications
have quite large memory requirements. By using a daemon process, this
shifts the memory overhead to the daemon processes and the main Apache
child processes will not be affected.

If needing to run !TurboGears as a different user than that which Apache
runs its child processes as, then the 'user' and 'group' options can be
supplied to the WSGIDaemonProcess directive when using daemon mode. If
running as a distinct user it would generally not be necessary to
explicitly indicate the location of a suitable cache directory for Python
eggs. This is because they will be automatically placed in the
'.python-eggs' subdirectory of the home directory of the user the process is
running as.
