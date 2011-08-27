=======================
Integration With Django
=======================

Note: This is not intended as a basic tutorial on how to setup mod_wsgi.
It is recommended you first read more introductory material for mod_wsgi.
Start by reading through various documents linked off
:doc:`InstallationInstructions`. If wanting to know
about source code reloading issues when running Django under Apache and
mod_wsgi then ensure you read :doc:`ReloadingSourceCode`.

The `Django <http://www.djangoproject.com/>`_ framework provides the
``django.core.handlers.wsgi.WSGIHandler()`` function for constructing a
WSGI application corresonding to a Django application. Using this function,
a script file for a Django application which is compatible with mod_wsgi
would be constructed as follows::

    import os, sys
    sys.path.append('/usr/local/django')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    
    import django.core.handlers.wsgi
    
    application = django.core.handlers.wsgi.WSGIHandler()

The directory added to ``sys.path`` would be the directory containing the
package for the Django site created by running::

    django-admin.py startproject mysite

In other words, it should be the directory you were in when
'django-admin.py' was run. It also equates to the parent
directory of the directory which contains the 'settings.py' created by
'django-admin.py startproject'.

Note that this directory should never be created under !DocumentRoot of the
Apache installation or any other directory exposed via Apache web server.

Where you called your project something other than 'mysite', you should adjust
the value of 'DJANGO_SETTINGS_MODULE' above as appropriate. Similarly, for
any configuration below which mentions 'mysite' replace that with the actual
name of your project.

If you get an error of the following form in the Apache error logs, where
'mysite.settings' is what ever value you ended up using in
'DJANGO_SETTINGS_MODULE', then you haven't used the correct directory when
setting up ``sys.path``::

    [Tue May 05 19:10:51 2009] [error] [client 127.0.0.1] \
     raise ImportError, "Could not import mysite.settings '%s' \
     (Is it on sys.path? Does it have syntax errors?): %s" \
     % (self.SETTINGS_MODULE, e)

If you have been using the Django development server and have made use of
the fact that it is possible when doing explicit imports, or when
referencing modules in 'urls.py', to leave out the name of the site and use
a relative module path, you will also need to add to ``sys.path`` the
path to the site package directory itself::

    sys.path.append('/usr/local/django')
    sys.path.append('/usr/local/django/mysite')

In other words, you would have the path to the directory containing the
'settings.py' file created by 'django-admin.py startproject', as well as
the parent directory of that directory, as originally added above.

Note that it is not recommended to be setting 'DJANGO_SETTINGS_MODULE' to
be 'settings' and only listing the path to the directory containing the
'settings.py' file. This is because such a setup will be divergent from
how the Django development sets it and everything may not work as expected.

Also, be aware that the Django development server does a lot of other
preconfiguration and preimporting that the supplied WSGI handler from
Django doesn't do. This means that even where you add both directories to
'sys.path' and set 'DJANGO_SETTINGS_MODULE' qualified by project directory
name, code which works under the Django development server will not work
with the Django WSGI handler.

There is some dispute as to whether this is a flaw in the Django WSGI
handler or whether the real problem is that the code which doesn't work was
using Django in a manner which it shouldn't. Thus, if you find you have
code which works under the Django development server but not via the WSGI
handler, ensure you read:

  http://blog.dscpl.com.au/2010/03/improved-wsgi-script-for-use-with.html

This blog post will outline why the two hosting mechanisms work differently.
Based on that, you can try the alternate WSGI script file outlined at the
end of that post.

As to the Apache configuration itself, one example of how Apache could be
configured would be::

    Alias /media/ /usr/local/django/mysite/media/
    
    <Directory /usr/local/django/mysite/media>
    Order deny,allow
    Allow from all
    </Directory>
    
    WSGIScriptAlias / /usr/local/django/mysite/apache/django.wsgi
    
    <Directory /usr/local/django/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>

The configuration shown presumes that media files have been copied into a
subdirectory of the 'mysite' package called 'media'. Note that you do not
need to use the '!SetHandler None' hack on any directory holding static
files as is required in mod_python. When using mod_wsgi the Alias directory
works properly and will take precedence over the application.

It is also assumed that an 'apache' subdirectory has been created
within the package and the script file stored there under the name
'django.wsgi'. It is recommended that the name 'django.wsgi' always be
used. Definitely do not call it 'django.py' as by doing so Python may
mistakenly think it is the Django package itself if it is placed somewhere
on ``sys.path``.

Note that you should not go placing the 'django.wsgi' file in the same
directory as the 'settings.py' file, always use a subdirectory. This is
because Apache is being configured to allow serving of files from that
subdirectory. If you put it in the same directory as the 'settings.py' file,
you would be inadvertantly allowing Apache to serve up your source code if
someone accidentally mapped a URL to some parent directory of your project.

In other words, using an 'apache' subdirectory with the 'django.wsgi' file
being the only thing in it is more secure. For similar reasons, you should
never place any 'settings.py' file, even if named something else, in the
'apache' subdirectory. This is because that file may contain database passwords
and being in that directory Apache would be able to serve it up to clients
if someone accidentally mapped a URL to some parent directory of that
directory.

When running Django sites using mod_wsgi embedded mode, the applications
will run as the same user that the Apache child processes run as. If it
is desired that each Django instance run as a distinct user, the mod_wsgi
daemon mode should instead be used.

To enable daemon mode for a specific application the configuration need
only be augmented with directives to define the daemon process and delegate
the application to that process::

    WSGIDaemonProcess site-1 user=user-1 group=user-1 threads=25
    WSGIProcessGroup site-1

    Alias /media/ /usr/local/django/mysite/media/

    <Directory /usr/local/django/mysite/media>
    Order deny,allow
    Allow from all
    </Directory>

    WSGIScriptAlias / /usr/local/django/mysite/apache/django.wsgi

    <Directory /usr/local/django/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>

The default number of processes created when using WSGIDaemonProcess is
one. More processes can be defined using the 'processes' option to the
directive. Do not however use 'processes=1' to indicate a single process
unless you are specifically running a cluster of Apache servers, in a load
balanced configuration, with only a single process hosted on each. This is
because the use of the 'processes' option has the side effect of setting
'wsgi.multiprocess' variable in WSGI environment to 'True'. Certain in
browser WSGI debuggers will check that variable and will not run if they
think it is a multi process configuration, albeit if you only have one
server and the one process they could actually still run if not for that
flag.

Note that Django expects the name of the site settings file to be stored in
the environment variable ``DJANGO_SETTINGS_MODULE``. This means that it
is impossible to run two Django sites within one Python sub interpreter.
This isn't in general a problem with mod_wsgi however, as the default for
mod_wsgi is to execute each WSGI application within the context of its own
Python sub interpreter.

That mod_wsgi separates WSGI applications in this way should mean it is
possible to run multiple Django applications under the same !VirtualHost at
different mount points. Unfortunately, Django's WSGI adapter prior to alpha
versions of version 1.0, do not honour properly the WSGI ``SCRIPT_NAME``
environment variable, instead ignoring it and expecting the full request
URI to be in ``PATH_INFO``.

This issue and the problems it causes has been raised in Django ticket
`#285 <http://code.djangoproject.com/ticket/285>`_. Related problems that
effectively stem from the same issue have also been raised in Django
tickets `#2407 <http://code.djangoproject.com/ticket/2407>`_ and
`#1516 <http://code.djangoproject.com/ticket/1516>`_.

A change to Django which addresses this issue and which has been incorporated
into Django 1.0 is described in Django ticket
`#8015 <http://code.djangoproject.com/changeset/8015>`_. For older versions,
the workaround presented in Django ticket
`#2047 <http://code.djangoproject.com/ticket/2407>`_ can be used with the
script file being written as::

    import os, sys
    sys.path.append('/usr/local/django')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

    import django.core.handlers.wsgi

    _application = django.core.handlers.wsgi.WSGIHandler()

    def application(environ, start_response):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        return _application(environ, start_response)

With this change however, it will be necessary to ensure that any paths
listed in the Django ``urls.py`` file be prefixed with the value of
``SCRIPT_NAME`` minus the leading slash. For example where the mount
point is '/mysite' the URL patterns would need to be listed as::

    urlpatterns = patterns('',
         (r'^mysite/admin/', include('django.contrib.admin.urls')),
    )

As long as these changes are made however, it would then be possible to
host multiple Django applications at different mount points within the one
!VirtualHost. Remember though, these workarounds are only needed for Django
prior to Django 1.0 and only if mounting at a sub URL of the site and not
at the root of the site.

Note that the ``django.root`` option introduced in Django 1.0 alpha
versions does not apply to mod_wsgi and is only necessary with mod_python,
due to mod_python not setting ``SCRIPT_NAME`` correctly.

When setting up the Apache configuration for a site mounted at a sub URL,
the mount point must not have a trailing slash::

    WSGIScriptAlias /mysite /usr/local/django/mysite/apache/django.wsgi

A mass hosting like arrangement could also be set up using an Apache
configuration like the following::

    AliasMatch ^/([^/]+)/media/(.*) /usr/local/django/$1/media/$2

    <DirectoryMatch ^/usr/local/django/([^/]+)/media>
    Order deny,allow
    Allow from all
    </DirectoryMatch>

    WSGIScriptAliasMatch ^/([^/]+) /usr/local/django/$1/apache/django.wsgi

    <DirectoryMatch ^/usr/local/django/([^/]+)/apache>
    Order deny,allow
    Allow from all
    </DirectoryMatch>

When a new Django instance needs to be added, its package directory should
be created along with the 'media' and 'apache' directories as described.
Having done that, the site will be automatically available without needing
to restart Apache.

Note that changes will also be required in the Django ``settings.py``
file for each site. For example, the ``ADMIN_MEDIA_PREFIX`` setting will
need to be customised for each site to reflect where the media for that
site is located. Also, by default Django uses the same cookie name for the
session cookie for all sites. Thus it will be necessary to override the
``SESSION_COOKIE_NAME`` setting. It would be preferable that the
``path`` of the session cookie could be set through a
``SESSION_COOKIE_PATH`` setting as described in Django ticket
`#4724 <http://code.djangoproject.com/ticket/4724>`_. This would for example
allow the cookie scope to be restricted to the mount point of the site.

Note that prior to revision
`#6428 <http://code.djangoproject.com/changeset/6428>`_ of Django, the HTTPS
detection done by Django was wrong for WSGI and the internal
``is_secure()`` function returned the wrong result in some configurations
of Apache. To work around this problem you should use a WSGI application
wrapper to setup the WSGI environment how Django was expecting it::

    import os, sys
    sys.path.append('/usr/local/django')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

    import django.core.handlers.wsgi

    _application = django.core.handlers.wsgi.WSGIHandler()

    def application(environ, start_response):
        if environ['wsgi.url_scheme'] == 'https':
            environ['HTTPS'] = 'on'
        return _application(environ, start_response)

Now, traditional wisdom in respect of Django has been that it should
perferably only be used on single threaded servers. This would mean for
Apache using the single threaded 'prefork' MPM on UNIX systems and avoiding
the multithreaded 'worker' MPM. Problem with this advice is that the
'winnt' MPM on Windows systems is multi threaded, yet no advice is given in
regard to avoiding the use of Apache on Windows. There are also
instructions for using Django on top of FASTCGI hosting mechanism in a
multi threaded configuration, yet no warnings are provided that this may
cause problems.

On face value therefore, one might assume that Django itself does not
actually have specific problems when used with a multi threaded server
configuration. Unfortunately no definitive statement has been made by
the Django developers that this is the case or not. Recent investigations
by third parties are however starting to uncover some issues related to
multithreading:

  http://code.djangoproject.com/wiki/DjangoSpecifications/Core/Threading

Thus for now, it may well still be advisable to only use a single threaded
configuration for hosting Django. Ultimately though, you would really need
to analyse the information about threading problems to see if you are
using any of the affected functional components. You should also test your
own application code to see if it itself is thread safe. After doing that,
then you might find that for your particular application everything is
okay after all, and thus it may be safe to use Django in conjunction with
any of 'prefork', 'worker' or 'winnt' MPMs.

If problems are found with a specific application not being multi thread
safe, then using Apache on Windows wouldn't be possible at all, nor would
using mod_wsgi in embedded mode be advisable when Apache is using the
'worker' MPM on UNIX. In this later case though, daemon mode of mod_wsgi
could be used to delegate the Django application to a separate set of
daemon processes running in a multi process, but not multithreaded
configuration::

    WSGIDaemonProcess site-1 user=user-1 group=user-1 processes=5 threads=1
    WSGIProcessGroup site-1

    WSGIScriptAlias / /usr/local/django/mysite/apache/django.wsgi

    <Directory /usr/local/django/mysite/apache>
    Order deny,allow
    Allow from all
    </Directory>

Note that it is believed that any multithreading issues have been resolved
in Django 1.0 and so that version should be be safe to use in a multithread
configuration. As always, you still need to test your own code to determine
that it is multithread safe. You should also ensure to consult the threading
issues document referenced above.

A final note, there should never be a need to set 'FORCE_SCRIPT_NAME in
Django settings file when using mod_wsgi. If you find yourself having to do
that, you have done something wrong with configuring mod_wsgi or you have
incorrectly set up your patterns in your 'urls.py' file.

For other suggestions regarding how to configure mod_wsgi specifically
for Django, also check out the Django page at:

  http://code.djangoproject.com/wiki/django_apache_and_mod_wsgi
