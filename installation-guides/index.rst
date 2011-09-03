===================
Installation Guides
===================

The Apache/mod_wsgi package is :doc:`downloadable <../download-the-software>`
as C source code. This needs to be configured and compiled against the
specific version of Apache and Python that you wish to use. Instructions
for building from source code on UNIX systems can be found in:

* :doc:`building-from-source-code`

If you are running Windows, then precompiled 32 bit binaries are also
available for :doc:`download <../download-the-software>` for the latest
version of Apache and the more popular versions of Python. Instructions for
installing the binaries, as well as how to build a binary from source code
can be found in:

* :doc:`installation-on-windows`

After having got mod_wsgi built, installed and loading into Apache you
should validate that it is working properly using a simple WSGI hello world
program. A quick guide to configuring mod_wsgi for a WSGI hello world
application can be found in:

* :doc:`../configuration-guides/running-a-basic-application`

If rather than build mod_wsgi from source code you are wanting to find
precompiled binaries for a UNIX system, or if building from source code and
are experiencing problems, then check out the respective documentation for
your platform listed below.

* :doc:`installation-on-linux`
* :doc:`installation-on-macosx`
* :doc:`installation-on-solaris`
* :doc:`installation-on-freebsd`

If you have any problem with installing mod_wsgi or running the WSGI hello
world application, check out the following documents:

* :doc:`../frequently-asked-questions/index`
* :doc:`../installation-issues/index`
* :doc:`../configuration-issues/index`

If all worked okay for the WSGI hello world application, then you can learn
about more complex configuration of mod_wsgi or integrating your own WSGI
application based on a third party or custom framework by reading:

* :doc:`../configuration-guides/index`
