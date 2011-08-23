

=====================
Performance Estimates
=====================

Providing benchmarks comparing one system to another is always dangerous,
especially when they use different technologies. This is because the
performance can be dependent on how the system is setup or tested and what
the hardware configuration and operating system used is.

Because of that, performance estimates here will only deal with the
different means that WSGI applications can be hosted under Apache and where
the same base Apache configuration is used for all tests. It does not try
and provide a comparison to other systems which do not use Apache as the
web server.

In order to provide some reference point however, a normalised figure of
1000 requests/sec for serving up static files through Apache is used as a
baseline, with the different means of supporting a WSGI application through
Apache expressed relative to that value. If you really want to try and draw
some comparisons with another system, then determine this figure for Apache
on your system and extrapolate from that. Do keep in mind though that the
performance of Apache for different configurations can be quite different
and the result may not really tell you much.

The actual figures given here were derived from testing with Apache 2.2
(prefork) and the Apache "ab" program. Neither keep alive or concurrency
were used, meaning that the results reflect sequential requests using
different socket connections for each request. As such, the results should
be less influenced by how Apache may have been configured. Even so, various
factors can still mean that between separate runs of the same test, the
figures can jump around a fair bit. Thus the figures have been averaged and
rounded to give as described what is more an estimate of the relative
performance to the other mechanisms than a definitive indicator of
performance for the specific mechanism.

In all cases, the particular WSGI application which was used for testing
was as follows:

::

    def application(environ, start_response):
        status = '200 OK'
        output = 'Hello World!'
    
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
    
        return [output]


Note that because of its simplicity, this in practice is not going to be a
realistic indicator of overall performance of a WSGI application. A real
world application is likely to be much more complicated than this, and
possibly want to read content sent by a client, access databases, make use
of templating systems etc. All these extras increase overhead and will slow
down actual throughput for an application. So, to reiterate what has been
stated above, the figures here should only be used to compare relative
performance of the different mechanisms for hosting WSGI applications under
Apache. They are not going to give you an indication of how well a
particular application may run.

Static File Testing
-------------------

The static file test used as a baseline consisted of placing a file in the
directory specified as the document root for the Apache installation. This
contained the text 'Hello World!'. The throughput for this test was
normalised to being 1000 requests/sec. Subsequent results have been
adjusted in the same proportion to make it easier to compare the different
values.

Test Of mod_cgi Adapter
-----------------------

For the CGI test, the WSGI adapter listed in the WSGI PEP was used. This
was placed in the same file as the actual WSGI application. The Apache
configuration used was:

::

    ScriptAlias /mod_cgi/hello /usr/local/wsgi/scripts/hello.py
    
    <Directory /usr/local/wsgi/scripts>
    AllowOverride None
    Options None
    Order deny,allow
    Allow from all
    </Directory>


The result of the test gave an adjusted figure of 10 requests/sec. In other
words, static files could be served up 100 times quicker than running the
CGI script to generate the same value.

Note that the CGI test involves spawning a separate process to run the CGI
script. Different platforms may be more efficient at spawning such a
process and thus may give different relative performance than the
particular platform used.

Test Of mod_python Adapter
--------------------------

For the mod_python test, the WSGI adapter provided with Paste was used. The
Apache configuration used was:

::

    <Location "/mod_python/hello">
    SetHandler mod_python
    PythonHandler paste.modpython
    PythonAutoReload Off
    PythonPath "sys.path+['/usr/local/wsgi/scripts']"
    PythonOption wsgi.application hello::application
    PythonOption SCRIPT_NAME /mod_python/hello
    </Location>


Module reloading in mod_python was explicitly turned off, however, even if on
it would not have changed the results because the root module specified by
the ``PythonHandler`` directive was not a candidate for module reloading
and wasn't being changed either.

The result of the test gave an adjusted figure of 400 requests/sec.

Test Of mod_wsgi Adapter
------------------------

For the mod_wsgi adapter, the mod_wsgi equivalent to the mod_cgi
``ScriptAlias`` directive is used. The Apache configuration for this was:

::

    WSGIScriptAlias /mod_wsgi/hello /usr/local/wsgi/scripts/hello.py
    
    <Directory /usr/local/wsgi/scripts>
    AllowOverride None
    Options None
    Order deny,allow
    Allow from all
    </Directory>


The result of the test gave an adjusted figure of 900 requests/sec.

Because the ``WSGIScriptAlias`` directive can only be used in the main
Apache configuration file, it cannot be used to enable mod_wsgi from within
a '.htaccess' file. For this the ``SetHandler/AddHandler`` directives can
instead be used. The Apache configuration within the '.htaccess' file when
``SetHandler`` is used would be:

::

    SetHandler wsgi-script


The result of a test where a ".htaccess" file is used gives an adjusted
figure of 850 requests/sec. This reflects the additional overhead of Apache
having to map a URL against the filesystem and parsing the ".htaccess" file
for every request.

Where there is a need to run a WSGI application in its own distinct daemon
process and/or as a distinct user different from what Apache would normally
run as, the ``WSGIDaemonProcess`` and ``WSGIProcessGroup`` directives
can be used to setup the daemon process and delegate the WSGI application
to that process group.

The Apache configuration for the most basic scenario with a single daemon
process with only one thread being used would be:

::

    WSGIDaemonProcess daemon processes=1 threads=1
    
    WSGIScriptAlias /mod_wsgi/hello /usr/local/wsgi/scripts/hello.py
    
    <Directory /usr/local/wsgi/scripts>
    WSGIProcessGroup daemon
    AllowOverride None
    Options None
    Order deny,allow
    Allow from all
    </Directory>


The result of a test running with this configuration gave an adjusted
figure of 700 requests/sec. The extra overhead in this circumstance is due
to the need to proxy the request to the daemon process and subsequently
proxy the response back through the Apache child process and then back
to the client making the request.

Note that the figure of 700 requests/sec was obtained using version 2.0c5
of mod_wsgi. Prior to this version only 500 requests/sec were being
achieved, however a peformance bottleneck in relation to the proxy code was
eliminated in the newer version, thus improving the result.

Summary Of Results
------------------

The results can be summarised as follows:

|| *Mechanism* || *Requests/sec* ||
||mod_cgi (``ScriptAlias``)||10||
||mod_python (``PythonHandler``)||400||
||mod_wsgi (``WSGIDaemonProcess``)||700||
||mod_wsgi (``.htaccess/SetHandler``)||850||
||mod_wsgi (``WSGIScriptAlias``)||900||
||static (``DocumentRoot``)||1000||

Basic guidance would thus be that the overhead of mod_wsgi when running in
its most efficient mode is half that of mod_python and significantly less
than when using CGI.

Do note though that any gain in performance over mod_python will be
immediately swallowed up as soon as you load up one of the large Python web
frameworks such as Django or !TurboGears. This will especially be the case
where a database backend is being used and is because most of the overhead
will then derive from the Python web framework and any bottlenecks in
accessing the database. Any overhead from mod_wsgi will be a very small
component of the total and so any gain in that area will hardly be noticed.

Thus, for a large Python web framework you would not expect to see much
difference to mod_python. Only when using frameworks with less overhead or
where no database access is involved would you expect to see noticeable
gains over using mod_python. Similarly, you wouldn't see any real
difference between embedded mode and daemon mode of mod_wsgi. For that
matter, all WSGI hosting mechanisms are going to have not that dissimilar
performance for a large Python web framework.

Do note however that although raw performance of running mod_wsgi in
embedded mode is slightly better than daemon mode, the default MPM settings
of Apache would need to be adjusted and WSGI application preloading used to
ensure that best performance is still achieved.

The problem with Apache in embedded mode is that its default MPM settings
aren't really set up for a persistent dynamic web site. The main issue is
that the settings define a minimal number of Apache child processes to be
used for handling requests. If the load increases, only then would Apache
create additional child processes to handle the increased number of requests.

This mechanism may be fine for handling of static file requests where the
startup costs of additional child processes are neglible, but not for a fat
dynamic web application with significant startup costs. For the latter, to
ensure best performance it would be necessary to configure Apache with a
much higher initial number of child processes, possibly even for that
number to be fixed at the defined maximum.

As well as ensuring enough child processes are always available, the Python
web application should also be preloaded so that it is already resident
when the first requests arrives. If this is not done, then the first
request that arrives would stall until the application had loaded. Any
other requests that arrive at the same time and which are handled by that
same process would similarly stall until initialisation of the application
had completed.

If these steps are not taken, then embedded mode would give the appearance
of performing worse than daemon mode when technically that should not be
the case. The main issue one would see is a spike in processor load when
Apache decided to create additional child processes to handle an increased
number of requests. As this would occur when the processor is already
starting to come under load due to the increasing level of requests, it
would initially further slow the system down, thus hindering rather than
helping the situation.

In the worst case scenario, if the startup costs are significant enough,
the act of Apache creating the additional child processes would only serve
to completely overload the machine and make it unresponsive, just when you
dont need that to happen.

This behaviour of embedded mode is no different to what one would see if
one was using mod_python and similarly had not adjusted the Apache MPM
settings to values more appropriate for a fat persistent dynamic web
application. Part of the reason mod_python has got such a bad reputation in
the past, and why mod_wsgi embedded mode is being said to be no better than
mod_python, has thus more to do with Apache not being configured correctly
than the respective Apache modules or modes they support.

Overall, if you are not adept at configuring Apache properly, then the
safest option is to use mod_wsgi daemon mode. If using Windows, where only
embedded mode is available, do note though that none of this is an issue
anyway as on Windows there is only one child process for handling requests
and no extra processes are created.
