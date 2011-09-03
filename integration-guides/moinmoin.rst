=========================
Integration With MoinMoin
=========================

Note: Requires MoinMoin 1.5 or later.

Note: This is not intended as a basic tutorial on how to setup mod_wsgi.
It is recommended you first read more introductory material for mod_wsgi.
Start by reading through various documents linked off
:doc:`../installation-guides/index`.

The `MoinMoin <http://moinmoin.wikiwikiweb.de/>`_ application provides the
``MoinMoin.server.wsgi.moinmoinApp()`` function for running MoinMoin as a
WSGI application. Using this function, a script file for a MoinMoin
application which is compatible with mod_wsgi would be constructed as
follows::

    import sys
    sys.path.insert(0, '/usr/local/moin/mywiki')

    from MoinMoin.server.wsgi import moinmoinApp

    application = moinmoinApp

The root directory for the wiki and that which contains ``wikiconfig.py``
needs to be added to ``sys.path``.

One example of how Apache could be configured would be::

    Alias /wiki/ /usr/local/share/moin/htdocs/

    <Directory /usr/local/share/moin/htdocs>
    Order deny,allow
    Allow from all
    </Directory>

    WSGIScriptAlias /mywiki /usr/local/moin/mywiki/apache/mywiki.wsgi

    <Directory /usr/local/moin/mywiki/apache>
    Order deny,allow
    Allow from all
    </Directory>

The configuration shown presumes that an 'apache' subdirectory has been
created within the wiki site instance and the script file stored there
under the name 'mywiki.wsgi'.

Although MoinMoin has its own mechanism for creating a wiki farm, you can
still use Apache and mod_wsgi to create a mass hosting like configuration.
You may want to do this where each wiki needs to have a different set of
plugins or you do not want any Python data objects shared between each
wiki. Separation in this latter respect is achieved by virtue of the fact
that mod_wsgi will by default execute each WSGI application script within
its own Python sub interpreter.

A suitable Apache configuration for this arrangement would be as follows::

    Alias /wiki/ /usr/local/share/moin/htdocs/

    <Directory /usr/local/share/moin/htdocs>
    Order deny,allow
    Allow from all
    </Directory>

    WSGIScriptAliasMatch ^/sites/([^/]+) /usr/local/moin/$1/apache/$1.wsgi

    <DirectoryMatch ^/usr/local/moin/([^/]+)/apache>
    Order deny,allow
    Allow from all
    </DirectoryMatch>

When a new MoinMoin site needs to be added, it would be created along with
the 'apache' directory containing an appropriate script configured for that
MoinMoin instance. Having done that, the site will be automatically
available without needing to restart Apache.

For other suggestions regarding how to configure mod_wsgi specifically
for MoinMoin, also check out the MoinMoin page at:

  http://moinmaster.wikiwikiweb.de/HelpOnInstalling/ApacheWithModWSGI
