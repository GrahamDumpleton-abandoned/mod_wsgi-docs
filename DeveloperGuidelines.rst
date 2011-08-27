====================
Developer Guidelines
====================

After having installed and configured mod_wsgi you will want to know how to
get the most out of it. This document links to documentation on this site
and elsewhere relevant to the developer of WSGI applications in general and
in particular WSGI applications being hosted on mod_wsgi.

The most important document is the WSGI specification itself. This can
be found at:

  http://www.python.org/dev/peps/pep-0333/

This defines the interface specification that WSGI applications and WSGI
adapters for web servers, such as mod_wsgi, are supposed to adhere to.
Additional information about WSGI in general can be found on the WSGI wiki
at:

  http://www.wsgi.org/wsgi

If you have quite specific questions about the WSGI specification, you
should ask on the Python WEB-SIG mailing list.

  http://groups.google.com/group/python-web-sig

If you are using a particular Python web framework to implement your
application, you might also want to ask your questions on the relevant
mailing lists for those packages if it relates more to the package
rather than the WSGI specification or mod_wsgi.

If on the other hand your problems do appear to relate more to mod_wsgi,
first off ensure that you read the following documents.

* :doc:`InstallationIssues`
* :doc:`ConfigurationIssues`
* :doc:`ApplicationIssues`

If none of the common issues match up with the problem you are seeing and
you have the need to perform more low level debugging, check out the
following documents.

* :doc:`DebuggingTechniques`

You can also do some basic checking of your installation and configuration
to validate that how it is setup is how you expect it to be. See the
following documents.

* :doc:`CheckingYourInstallation`

If you are still having no joy and need further assistance then ask any
questions you have on the mod_wsgi mailing list at:

  http://groups.google.com/group/modwsgi

If you want to know more about some of the inner workings of mod_wsgi,
how it is implemented and how it interacts with Apache read the following
documents.

* :doc:`ProcessesAndThreading`
* :doc:`VirtualEnvironments`

* :doc:`ReloadingSourceCode`
* :doc:`RegisteringCleanupCode`

* :doc:`FileWrapperExtension`
* :doc:`AccessControlMechanisms`

* :doc:`TipsAndTricks`

If you want to know more detail about some of the problems that can arise
when running WSGI applications on top of mod_wsgi read the following
documents.

* :doc:`IssuesWithExpatLibrary`
* :doc:`IssuesWithPickleModule`
