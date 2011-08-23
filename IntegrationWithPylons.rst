

=======================
Integration With Pylons
=======================

_Note: This is not intended as a basic tutorial on how to setup mod_wsgi.
It is recommended you first read more introductory material for mod_wsgi.
Start by reading through various documents linked off
[InstallationInstructions Installation Instructions]._

The [http://pylonshq.com/ Pylons] framework provides the
``paste.deploy.loadapp()`` function for constructing a WSGI application
stack based on a specific configuration file. Using this function, a script
file for a Pylons application which is compatible with mod_wsgi would be
constructed as follows:

::

    import os, sys
    sys.path.append('/usr/local/pylons/mysite')
    os.environ['PYTHON_EGG_CACHE'] = '/usr/local/pylons/python-eggs'
    
    from paste.deploy import loadapp
    
    application = loadapp('config:/usr/local/pylons/mysite/development.ini')


The directory added to ``sys.path`` would be the directory created by
running:

::

    paster create --template=pylons mysite


Because an application is run as the user that Apache runs as, if Python
eggs are being used and there is a need for eggs to be unpacked on the fly,
it may not have the ability to create a cache directory in the default
location. Therefore, it may be necessary to set the environment variable
``PYTHON_EGG_CACHE`` at the start of the script file to an appropriate
directory where the Apache user has write permission and into which it can
unpack egg files.

One example of how Apache could be configured would be:

::

    WSGIScriptAlias /mysite /usr/local/pylons/mysite/apache/mysite.wsgi
    
    <Directory /usr/local/pylons/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>


The configuration shown presumes that an 'apache' subdirectory has been
created within the Pylons site instance and the script file stored there
under the name 'mysite.wsgi'.

Note that you may not be able to use the 'Interpreter' option for the
WSGIReloadMechanism directive when using Pylons. This is because some
versions of Pylons make use of the !PyProtocols package and it is not able
to cope with sub interpreters being destroyed and a new sub interpreter
being created, from which the !PyProtocols package is once again being
used.

Although newer versions of Pylons may not make direct use of the
!PyProtocols package, you can still encounter problems because of
!PyProtocols being used indirectly when packages such as !RuleDispatch are
present and that is loaded directly by your application or indirectly via
packages such a !TurboJson. Even the Pylons 'helloworld' example triggers
loading of JSON code and so if !TurboJson is present it will fail to work
with 'Interpreter' reloading. The large level of interdepencies between
packages when using Pylons in a large application may make it quite hard to
avoid the problem.

The result of attempting to use the 'Interpreter' option will be
unpredictable, but can range from the Apache child process crashing to
random Python exceptions. The actual problems seem to stem from the use of
Pyrex generated C code in !PyProtocols. At this stage it is not known
whether the problems are with how !PyProtocols uses Pyrex, or whether Pyrex
itself doesn't generate code which is safe to use with multiple sub
interpreters.

For further suggestions on how to configure mod_wsgi specifically for
Pylons, check out the following pages:

  http://docs.pythonweb.org/pages/viewpage.action?pageId=5439610
