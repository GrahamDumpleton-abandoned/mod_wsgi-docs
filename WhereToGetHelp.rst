

=================
Where To Get Help
=================

If you are having problems with installing or using mod_wsgi, then ensure
you read this first. It will give you some pointers on what you can do to
resolve the problem yourself.

Read The Documentation
----------------------

First thing you should do is make sure you have read the actual mod_wsgi
documentation on the mod_wsgi site. The documentation on the mod_wsgi site
goes into much more detail than anything else you will find elsewhere on
the Internet. It certainly is going to be better to be relying on the
official documentation rather than some obscure personal blog site. Even
integration guides in official documentation for the major Python web
frameworks are quite sparse and in some cases inaccurate or incomplete.

The key document you should start with is:

  * [InstallationInstructions Installation Instructions]

This has pointers to other documents covering installation, configuration
and subsequent setup issues. Also references documents on how to go about
debugging any issues.

If you have been successful in getting mod_wsgi running and your questions
are more about how mod_wsgi works or how more complicated features are used,
then you should start with:

  * [DeveloperGuidelines Developer Guidelines]

Although this is labelled as being for developers, that is referring to you
as a user of mod_wsgi and a developer of your own web application. It isn't
information for people developing mod_wsgi itself.

You will find pointers to documentation in there about how mod_wsgi
processes and threading works, use of virtual environments, source code
reloading and much more.

For a lost of all available documentation see:

  * [http://code.google.com/p/modwsgi/w/list Documentation Index]

Also check the authors [http://blog.dscpl.com.au/ blog site] as various useful posts have been made there which have never made there way back into the core documentation.

Hello World Program
-------------------

Second thing is that if your issue is arising from your very first attempt
to setup mod_wsgi and you are trying to use a high level Python web
framework or application, then step back for a moment and try and get a
basic hello world program running first.

In other words, lets just make sure mod_wsgi itself is working before you
complicate matters by introducing some third party software into the picture.

You can find a simple hello world program in:

  * [QuickConfigurationGuide Quick Configuration Guide]

========================
Conference Presentations
========================

The author has also done a number of presentations in the past. The main one for which information is available online is as follows:.

  * [http://code.google.com/p/modwsgi/downloads/detail?name=mod_wsgi-pycon-sydney-2010.pdf PyCon Conference Slides - Sydney 2010]
  * [http://pyconau.blip.tv/file/3840484/ PyCon Conference Video - Sydney 2010]

Ensure you watch the presentatIon as it details many of the common pitfalls for new users.

Asking Your Questions
---------------------

Finally, if you still can't find the answer, next step is to use the
mod_wsgi mailing list to post your question. The mailing list is hosted by
Google Groups at:

  http://groups.google.com/group/modwsgi

You do not need to have a Google email account as Google Groups allows you
to register external email addresses as well.

Please use the mailing list in preference to raising a ticket in the issue
tracker unless you are somewhat certain that the problem is a bug in mod_wsgi
and not just some environment issue related to your application, any third
party packages being used or the operating system. It is much easier to have
a discussion on the mailing list than the issue tracker.

The mailing list also has many people participating, or at least reading,
so you have people with a broad experience with many third party Python web
packages and operating systems and so you aren't reliant on just the
mod_wsgi developers to try and answer any question.

If the problem is potentially more an issue with a third party package or
the operating system rather than mod_wsgi, you might also consider asking
on any mailing list related to the third party package instead. You will
find references to support mailing lists for many of the major Python web
frameworks and applications in the integration guides provided on the
mod_wsgi site.

A further option is to ask your question on
[http://stackoverflow.com/ StackOverflow], if a programming question, or
[http://serverfault.com/ ServerFault], if an administration issue. These
sites allow a broad range of questions about many topics with quite a large
user base of sometimes knowledgeable people. You might also try IRC
channels related to any third party package or the more general #wsgi and
#python.web channels.

Do be aware though that the only forum that is now monitored by mod_wsgi
developers is the mod_wsgi mailing list. Questions about mod_wsgi will no
longer be answered on sites such as !StackOverflow and !ServerFault, on
IRC, or even mailing lists for other packages. So, it is much preferable to
use the mod_wsgi mailing list if you want an informed answer for a mod_wsgi
specific question.

As a general rule, if you have never participated in public forums
previously to seek answers to technical questions, including about Open
Source software, it is highly recommended you have a read of.

  http://www.catb.org/esr/faqs/smart-questions.html

This will help you to ensure you have exhausted all possibilities as to
where to find information and try and solve the problem yourself, as well
as assist you in framing your question the best way so as to get the best
response possible. Remember that people on the mailing list are
volunteering their time to help and don't get paid for answering questions.
Thus, it is in your interest not to annoy them too much.

No matter which forum you use, when asking questions, it is always helpful
to detail the following:

1. Which version of mod_wsgi you are using and if using a packaged
distribution, who provided the distribution.

If you are not using the latest version, then upgrade first and verify the
problem still occurs with the latest version.

2. Which version of Python you are using and if using a packaged
distribution, who provided the distribution.

3. Which version of Apache you are using and if using a packaged
distribution, who provided the distribution.

If not using latest patch revision of Apache 2.2, then consider
upgrading and trying again.

4. What operating system you are using.

5. Details on any third party packages being used and what versions of
those packages.

6. The mod_wsgi configuration you are using from Apache configuration files.

In particular you should indicate whether you are using mod_wsgi embedded
mode or daemon mode. Also can be helpful to indicate what MPM Apache has
been compiled for and whether mod_php or mod_python are being loaded into
the same Apache instance.

7. Relevant error messages from the Apache error logs.

Specifically, don't just quote the single line you think shows the error
message. Instead, also show the lines before and after that point. These
other lines from the error logs may show supplemental error messages from
Apache or mod_wsgi or provide Python traceback information.

Lodging Bug Reports
-------------------

If you believe you really have uncovered a bug in mod_wsgi code, and that has
perhaps also been verfied through discussion on the mod_wsgi mailing list or
elsewhere, and the mod_wsgi developers don't beat you to it, then lodge a bug
report on the mod_wsgi issue tracker. The issue tracker is located at:

  http://code.google.com/p/modwsgi/issues/list

As mentioned above, try and resolve issues using the mod_wsgi mailing list
before lodging bug reports. The majority of issues lodged by non developers
via the issue tracker are not actually bugs in mod_wsgi but due to external
factors or simply a failure to read the documentation.

Contacting The Author
---------------------

It would be prefered that you use the mod_wsgi mailing list to ask questions.
If however it involves revealing information which is confidential then you
can always track down the author's email address and make contact direct. This
really should be a last resort.

If the question doesn't seem to warrant personal contact being made, you will
be told to use the mod_wsgi mailing list like everyone else. That will be
reconsidered if you want to pay some sort of support money for mod_wsgi or
give a generous [HowToContributeBack donation].
