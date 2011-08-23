====================
WSGIPythonExecutable
====================

+----------------+-----------------------------------------------------------+
| Description    | Absolute path to Python executable.                       |
+----------------+-----------------------------------------------------------+
| Syntax         | ``WSGIPythonExecutable`` *file-path*                      |
+----------------+-----------------------------------------------------------+
| Context        | server config                                             |
+----------------+-----------------------------------------------------------+

**Note: The WSGIPythonExecutable directive described here has been removed
in mod_wsgi version 2.0. The WSGIPythonHome directive should be used
instead.**

Can be used to define the location of the Python executable. This should
only need to be defined where the Python executable is not in the
``PATH`` of the user that Apache runs as, or where a system has multiple
versions of Python installed in different locations in the file system,
especially different installations of the same major/minor version, and the
installation that Apache finds in its ``PATH`` is not the desired one.

When this directive is used to define the location of the Python executable,
the Python executable is not actually executed. Instead, Python when
initialised uses this location as a starting point to try and determine
where its library files are installed.

For some platforms, this directive is the same as having set the
environment variable ``PYTHONEXECUTABLE`` in the environment of the user
that Apache executes as. If this directive is used it will override any
setting of ``PYTHONEXECUTABLE`` in the environment of the user that
Apache executes as.

This directive is not available on the Windows platform. Any problems on
the Windows platform should be resolved by appropriate changes to the
Windows registry.

This directive will have no affect if mod_python is being loaded into Apache
at the same time as mod_wsgi as mod_python will in that case be responsible
for initialising Python.

