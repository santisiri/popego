"""Authenticate Single Sign-On Middleware

==============
Single-Sign On
==============

About SSO
---------

Single sign on is a session/user authentication process that allows a user to
provide his or her credentials once in order to access multiple applications. 
The single sign on authenticates the user to access all the applications he or
she has been authorized to access. It eliminates future authenticaton requests 
when the user switches applications during that particular session.

.. admonition :: sources

    # http://searchsecurity.techtarget.com/sDefinition/0,,sid14_gci340859,00.html
    # http://en.wikipedia.org/wiki/Single_sign-on

AuthKit Implementations
-----------------------

The SSO sub-package of Authenticate implements various SSO schemes for
several University SSO systems as well as OpenID. In the future, additional
SSO schemes like LID may also be supported.

These systems sub-class the ``RedirectingAuthMiddleware`` from the api package
as they all utilize a similar scheme of authentcation via redirection with
back-end verification.

.. note::
    All University SSO work developed by Ben Bangert has been sponsered by
    Prometheus Research, LLC and contributed under the BSD license.
"""
