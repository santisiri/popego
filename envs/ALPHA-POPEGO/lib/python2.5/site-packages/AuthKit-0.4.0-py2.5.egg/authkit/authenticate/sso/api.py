"""SSO API's

This module supplies the common abstract redirection-based SSO system used by
a variety of University SSO systems.

Generally the SSO system will throw a redirect for the authentication to be
performed elsewhere. Upon the user being redirected back, a verification 
process will be done to ensure they actually logged on.

It's also possible for some SSO systems to have more full fledged sign-on 
systems that operate as middleware in addition to purely processing a sign-on
request.
"""
import logging

from elementtree import ElementTree
from paste.request import construct_url
from paste.util.converters import asbool
from paste.httpexceptions import HTTPNotFound, HTTPSeeOther, HTTPForbidden
from paste.wsgiwrappers import WSGIRequest

from authkit.authenticate.multi import MultiHandler, status_checker
from authkit.authenticate import AuthKitConfigError
from authkit.authorize import NotAuthenticatedError

log = logging.getLogger(__name__)

class LoginFailure(HTTPForbidden):
    """ The exception raised if the verification fails """


class RedirectingAuthHandler(object):
    """Handles generating redirect to SSO system
    
    This application should implement a ``redirect_url`` method that will
    generate a redirect URL to the
    """
    def __call__(self, environ, start_response):
        request = WSGIRequest(environ)
        url = self.redirect_url(environ)
        log.debug("Sending redirect to %s", url)
        return HTTPSeeOther(url).wsgi_application(environ, start_response)


class RedirectingAuthMiddleware(object):
    def __init__(self, app, **kwargs):
        """Subclass should save several basic variables
        
        The application object should be saved to self.app, and the path
        handling for URL dispatch should be in a dict saved to self.dispatch
        like so:
        
        .. code-block :: Python
            
            class MyRedirectMiddleware(RedirectingAuthMiddleware):
                def __init__(self, app, path, use_options=False):
                    self.app = app
                    self.protect = []
                    self.dispatch = {
                        '/verify':'verify',
                        '/process':'handle_process'
                    }
                    self.path = '/cas2'
                
                def verify(self, environ, start_response):
                    # called for /cas2/verify
                    pass
                
                def handle_process(self, environ, start_response):
                    # called for /cas2/process
                    pass
        """
        raise NotImplemented()
    
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        
        if path in self.dispatch:
            log.debug("Found %s in dispatch path, calling method %s", 
                      path, self.dispath[path])
            return getattr(self, self.path + 
                           self.dispatch[path])(environ, start_response)
        
        for route in self.protect:
            if path.startswith(route) and 'REMOTE_USER' not in environ \
               and 'type=' + self.type in environ['QUERY_STRING']:
                log.debug("Found %s in protection paths. No REMOTE_USER set,"
                          " running auth verify.", path)
                return self.verify(environ, start_response)
            elif path.startswith(route):
                return NotAuthenticatedError()(environ, start_response)
        
        log.debug("Path: %s not in protect list %s.", path, self.protect)
        return self.app(environ, start_response)
    
    def verify(self):
        """Perform verification of redirection"""
        raise NotImplemented()
    
    def redirect_url(self):
        """Construct the redirect URL"""
        raise NotImplemented()


def find_multi_app(app):
    """Walks an app assuming it is a middleware stack with apps glued on at 
    either self.app or self.application
    
    Returns a tuple of the MultiHandler app ref and the possibly new app 
    stack. If a multihandler app wasn't found, then it will be at the top of 
    the returned app.
    """
    tempref = app
    while not isinstance(tempref, MultiHandler):
        tempref = getattr(tempref, 'app', getattr(tempref, 'application', None))
        if tempref is None:
            app = MultiHandler(app)
            tempref = app
    return tempref, app
