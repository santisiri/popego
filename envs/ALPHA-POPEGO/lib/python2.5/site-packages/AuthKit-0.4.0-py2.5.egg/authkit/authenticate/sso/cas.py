"""CAS 1.0 and 2.0 SSO Implementation

This Authentication middleware handles CAS 1.0 and 2.0 authentication. The 
latter of which supports proxy service tickets in addition to direct client
service tickets.

Note that this does not implement proxy granting ticket requests, merely
CAS 2.0 service validation (which can take proxy tickets).

`Protocol Reference <http://www.ja-sig.org/products/cas/overview/protocol/index.html>`_
"""
import logging
import urllib

from authkit.authenticate.sso.api import *

log = logging.getLogger(__name__)

class AuthCASHandler(RedirectingAuthHandler):
    """CAS 1.0 and 2.0 Redirect Handler
    
    This small middleware piece handles generating the redirect URL for the
    CAS 
    """
    def __init__(self, app, authority, path='', use_cas2=False, protect=None):
        self.app = app
        self.authority = authority
        self.path = path
        self._cas2 = use_cas2
    
    def redirect_url(self, environ):
        kwargs = {'service': construct_url(environ, querystring='type=cas')}
        
        # XXX TODO: Store this for the middleware below, also look for a proxy
        #           granting ticket option to store that its desired
        if 'authkit.cas.renew' in environ:
            kwargs['renew'] = 'true'
        if 'authkit.cas.gateway' in environ:
            kwargs['gateway'] = 'true'
            
            # renew and gateway should not both be set at once according to
            # CAS protocol
            assert 'renew' not in kwargs
        
        args = urllib.urlencode(kwargs)
        return self.authority + "login?" + args

class AuthCASMiddleware(RedirectingAuthMiddleware):
    """CAS 1.0 and 2.0 Capable Authentication Handler"""
    def __init__(self, app, authority, use_cas2=False, path='', protect=None):
        self.app = app
        self.authority = authority
        self.type = 'cas'
        self._cas2 = use_cas2
        if use_cas2:
            self._authtype = 'CAS 2.0'
        else:
            self._authtype = 'CAS 1.0'
        self.protect = protect or []
        self.dispatch = {path + '/verify':'verify'}
        
    def verify(self, environ, start_response):
        req = WSGIRequest(environ)
        if 'ticket' not in req.GET:
            log.debug("No ticket found in request, unable to verify, returning"
                      "404 Not Found.")
            return HTTPNotFound().wsgi_application(environ, start_response)
        
        ticket = req.GET['ticket']
        
        service = construct_url(environ, querystring='type=cas')
        kwargs = {'service': service, 'ticket':ticket}
        if req.environ.get('authkit.sso.cas.renew'):
            kwargs['renew'] = 'true'
        args = urllib.urlencode(kwargs)
                
        # XXX TODO: Store whether renew was used for this request to ensure
        #           that the validation asks for it as well
        #           Also store whether a proxy ticket was requested and ask for
        #           it during validation
        if self._cas2:
            log.debug("Validating using CAS 2.0")
            
            # We use proxyValidate for CAS 2.0 because it will handle both
            # service and proxy ticket validation
            requrl = self.authority + "proxyValidate?" + args
            response = urllib.urlopen(requrl).read()
            log.debug("Raw response of auth verification: \n\t%s", response)
            tree = ElementTree.fromstring(response)
            valid = tree[0].tag.endswith('authenticationSuccess')
            results = {}
            if valid:
                log.debug("Successfully authenticated")
                user_kwargs = {}
                results['user'] = tree[0][0].text
                results['extra_environ'] = {}
                
                # Did we get a proxy ticket?
                if len(tree[0]) > 1 and tree[0][1].tag.endswith('proxyGrantingTicket'):
                    results['authkit.cas.proxyTicket'] = tree[0][1].text.strip()
                    
                    # Any proxies returned as well?
                    if len(tree[0] > 2):
                        proxies = [x.text.strip() for x in tree[0][2]]
                        results['authkit.cas.proxies'] = proxies                
            else:
                log.info('Authentication failed for auth: %s, ticket %s, '
                         'response: %s', self._authtype, ticket, 
                         tree[0].attrib['code'])
        else:
            log.debug("Validating using CAS 1.0")
            requrl = self.authority + "validate?" + args
            result = urllib.urlopen(requrl).read().split("\n")
            log.debug("Raw response of auth verification: \n\t%s", result)
            valid = 'yes' == result[0]
            results = {}
            if valid:
                results['user'] = result[1]
            else:
                log.info('Authentication failed for auth: %s, ticket %s, '
                         'response: %s', self._authtype, ticket, result[0])
        
        if not valid:
            log.debug("Invalid response, returning login failure.")
            return LoginFailure().wsgi_application(environ, start_response)
        environ['AUTH_TYPE'] = self._authtype
        environ['REMOTE_USER'] = results['user']
        
        set_user = req.environ.get('paste.auth_tkt.set_user')
        user_data = self._authtype
        if set_user:
            set_user(results['user'], user_data=user_data)
        
        # Add in optional environ data from the auth system
        if 'extra_environ' in results:
            environ.update(results['extra_environ'])
        
        log.debug("Authentication success, calling app.")
        return self.app(environ, start_response)

def make_cas_handler(app, auth_conf, app_conf=None, global_conf=None,
                     prefix='authkit.sso.cas'):
    if 'authority' not in auth_conf:
        raise AuthKitConfigError("No %sauthority key specified" % prefix)
    kwargs = dict(authority=auth_conf['authority'])
    if 'use_cas2' in auth_conf:
        kwargs['use_cas2'] = True
    kwargs['path'] = auth_conf.get('path', '')
    if 'path' in auth_conf:
        kwargs['path'] = auth_conf['path']
    if 'protect' in auth_conf:
        kwargs['protect'] = auth_conf['protect'].split(',')
    
    app = AuthCASMiddleware(app, **kwargs)
    multi_app, app = find_multi_app(app)
    multi_app.add_method('cas', AuthCASHandler, **kwargs)
    multi_app.add_checker('cas', status_checker)
    
    return app
