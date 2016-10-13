"""Highly flexible OpenID based authentication middleware

.. Note::

    If you want to test this module feel free to setup an account at
    passurl.com. The site is in alpha and any accounts will be deleted before
    launch but it might help with testing.

Full documentation on the use of this OpenID module is in the AuthKit manual.

.. warning ::

    Any data returned from an OpenID identity provider is stored in the cookie
    user data. This is not encryted when sent to the browser (unless you are 
    using a secure connection). Whilst this is unlikely to be a major problem 
    in your application it is something to be aware of.

This middleware actually sets two cookies, one for AuthKit and one for a session
store to store the ID which OpenID information is keyed against.
"""

import cgi
import paste.request
import string
import sys
from authkit.authenticate import AuthKitConfigError
from paste.request import construct_url
from openid.consumer import consumer
from openid.oidutil import appendArgs
from yadis.discover import DiscoveryFailure
from urljr.fetchers import HTTPFetchingError
from authkit.authenticate import get_template, valid_password, \
   get_authenticate_function, strip_base, RequireEnvironKey, \
   AuthKitUserSetter, AuthKitAuthHandler
from authkit.authenticate.multi import MultiHandler, status_checker
from beaker.middleware import SessionMiddleware

def template():
    return """\
<html>
  <head><title>Please Sign In</title></head>
  <body>
    <h1>Please Sign In</h1>
    <div class="$css_class">$message</div>
    <form action="$action" method="post">
      <dl>
        <dt>OpenID Passurl:</dt>
        <dd><input type="text" name="openid" value="$value"></dd>
      </dl>
      <input type="submit" name="authform" />
      <hr />
    </form>
  </body>
</html>
"""

def passurl_urltouser(environ, url):
    return url.strip('/').split('/')[-1]

def render(template, **p):
    if sys.version_info >= (2,4):
        return string.Template(template()).substitute(
            **p
        )
    else:
        for k, v in p.items():
            template = template().replace('$'+k, v)
        return template

class OpenIDAuthHandler(object):
    """
    This middleware is triggered when the authenticate middleware catches 
    a 401 response. The form is submitted to the verify URL which the other
    middleware handles
    """
    def __init__(self, app, template, path_verify, baseurl='', charset=None):
        self.app = app
        self.template = template
        self.baseurl = baseurl
        self.path_verify = path_verify
        if charset is None:
            self.charset = ''
        else:
            self.charset = '; charset='+charset

    def __call__(self, environ, start_response):
        baseurl = self.baseurl or construct_url(
            environ, 
            with_query_string=False, 
            with_path_info=False
        )
        content = render(
            self.template,
            message='',
            value='',
            css_class='',
            action=baseurl + self.path_verify
        )
        start_response(
            "200 OK",
            [
                ('Content-Type', 'text/html'+self.charset),
                ('Content-Length', str(len(content)))
            ]
        )
        return [content]

def make_store(store, config):
    conn = None
    if store == 'file':
        from openid.store import filestore
        cstore = filestore.FileOpenIDStore(config)
    elif store == 'mysql':
        import MySQLdb
        from DBUtils.PersistentDB import PersistentDB
        from openid.store.sqlstore import MySQLStore
        from sqlalchemy.engine.url import make_url
        
        def create_conn(dburi):
            url = make_url(dburi)
            p={'db':url.database}
            if url.username:
                p['user'] = url.username
            if url.password:
                p['passwd'] = url.password
            if url.host:
                p['host'] = url.host
            if url.port:
                p['port'] = url.port
            return PersistentDB(MySQLdb, 1, **p).connection()
        conn = create_conn(config)
        cstore = MySQLStore(conn)
    else:
        raise Exception("Invalid store type %r"%store)
    return conn, cstore
    
class AuthOpenIDHandler:
    """
    The template should be setup from authkit.open_id.template.file or 
    authkit.open_id.template.obj before we get here!
    """
    def __init__(
        self, 
        app, 
        store_type, 
        store_config, 
        baseurl, 
        path_signedin, 
        template=None,
        session_secret=None,
        session_key='authkit_openid',
        session_middleware='beaker.session',
        path_verify='/verify', 
        path_process='/process',
        urltouser=None,
        charset=None,
        sreg_required=None,
        sreg_optional=None,
        sreg_policyurl=None
    ):
        self.conn, self.store = make_store(store_type, store_config)
        self.baseurl = baseurl
        self.template = template
        self.path_signedin = path_signedin
        self.path_verify = path_verify
        self.path_process = path_process
        self.session_middleware = session_middleware
        self.session_key = session_key
        self.session_secret = session_secret
        self.app = app
        self.urltouser = urltouser
        if charset is None:
            self.charset = ''
        else:
            self.charset = '; charset='+charset
        self.sreg_required = sreg_required
        self.sreg_optional = sreg_optional
        self.sreg_policyurl = sreg_policyurl

    def __call__(self, environ, start_response):
        # If we are called it is because we want to sign in, so show the 
        if not environ.has_key(self.session_middleware):
            raise AuthKitConfigError(
                'The session middleware %r is not present. '
                'Have you set up the session middleware?'%(
                    self.session_middleware
                )
            )
        if environ.get('PATH_INFO') == self.path_verify:
            response = self.verify(environ, start_response)
            environ[self.session_middleware].save()
            return response
        elif environ.get('PATH_INFO') == self.path_process:
            response = self.process(environ, start_response)
            environ[self.session_middleware].save()
            return response
        else:
            return self.app(environ, start_response)

    def verify(self, environ, start_response):
        baseurl = self.baseurl or construct_url(
            environ, 
            with_query_string=False, 
            with_path_info=False
        )
        params = dict(paste.request.parse_formvars(environ))
        openid_url = params.get('openid')
        if not openid_url:
            response = render(
                self.template,
                message='Enter an identity URL to verify.',
                value='',
                css_class='',
                action=baseurl + self.path_verify
            )
            start_response(
                '200 OK', 
                [
                    ('Content-type', 'text/html'+self.charset),
                    ('Content-length', len(response))
                ]
            )
            return response
        oidconsumer = self._get_consumer(environ)
        try:
            request_ = oidconsumer.begin(openid_url)
        except HTTPFetchingError, exc:
            response = render(
                self.template,
                message='Error retrieving identity URL: %s' % (
                    cgi.escape(str(exc.why))
                ),
                value=self._quoteattr(openid_url),
                css_class='error',
                action=baseurl + self.path_verify
            )
            start_response(
                '200 OK', 
                [
                    ('Content-type', 'text/html'+self.charset),
                    ('Content-length', len(response))
                ]
            )
            return response
        except DiscoveryFailure, exc:
            response = render(
                self.template,
                message='Error retrieving identity URL: %s' % (
                    cgi.escape(str(exc[0]))
                ),
                value=self._quoteattr(openid_url),
                css_class='error',
                action=baseurl + self.path_verify
            )
            start_response(
                '200 OK', 
                [
                    ('Content-type', 'text/html'+self.charset),
                    ('Content-length', len(response))
                ]
            )
            return response
        else:
            if request_ is None:
                response = render(
                    self.template,
                    message='No OpenID services found for <code>%s</code>' % (
                        cgi.escape(openid_url),
                    ),
                    value=self._quoteattr(openid_url),
                    css_class='error',
                    action=baseurl + self.path_verify
                )
                start_response(
                    '200 OK', 
                    [
                        ('Content-type', 'text/html'+self.charset),
                        ('Content-length', len(response))
                    ]
                )
                return response
            else:
                trust_root = baseurl
                return_to = baseurl + self.path_process
                if self.sreg_required:
                    request_.addExtensionArg('sreg', 'required', self.sreg_required)
                if self.sreg_optional:
                    request_.addExtensionArg('sreg', 'optional', self.sreg_optional)
                if self.sreg_policyurl:
                    request_.addExtensionArg('sreg', 'policy_url', self.sreg_policyurl)

                redirect_url = request_.redirectURL(trust_root, return_to)
                start_response(
                    '301 Redirect', 
                    [
                        ('Content-type', 'text/html'+self.charset),
                        ('Location', redirect_url)
                    ]
                )
                return []

    def process(self, environ, start_response):
        baseurl = self.baseurl or construct_url(
            environ, 
            with_query_string=False, 
            with_path_info=False
        )
        value = ''
        css_class = 'error'
        message = ''
        params = dict(paste.request.parse_querystring(environ))
        oidconsumer = self._get_consumer(environ)
        info = oidconsumer.complete(dict(params))
        css_class = 'error'
        if info.status == consumer.FAILURE and info.identity_url:
            fmt = "Verification of %s failed."
            message = fmt % (cgi.escape(info.identity_url),)
            environ['wsgi.errors'].write(
                "Passurl Message: %s %s"%(message,info.message)
            )
        elif info.status == consumer.SUCCESS:
            username = info.identity_url
            user_data = str(info.extensionResponse( 'sreg' ))
            # Set the cookie
            if self.urltouser:
                username = self.urltouser(environ, info.identity_url)
            environ['paste.auth_tkt.set_user'](username, user_data=user_data)
            # Return a page that does a meta refresh
            response = """
<HTML>
<HEAD>
<META HTTP-EQUIV="refresh" content="0;URL=%s">
<TITLE>Signed in</TITLE>
</HEAD>
<BODY>
<!-- You are sucessfully signed in. Redirecting... -->
</BODY>
</HTML>
            """ % (self.baseurl + self.path_signedin)
            start_response(
                '200 OK', 
                [
                    ('Content-type', 'text/html'+self.charset),
                    ('Content-length', len(response))
                ]
            )
            return response
        elif info.status == consumer.CANCEL:
            message = 'Verification cancelled'
        else:
            environ['wsgi.errors'].write("Passurl Message: %s"%info.message)
            message = 'Verification failed.'
        value = self._quoteattr(info.identity_url)
        response = render(
            self.template,
            message=message,
            value=value,
            css_class=css_class,
            action=baseurl + self.path_verify
        )
        start_response(
            '200 OK', 
            [
                ('Content-type', 'text/html'+self.charset),
                ('Content-length', len(response))
            ]
        )
        return response

    #
    # Helper methods
    #

    def _get_consumer(self, environ):
        session = environ[self.session_middleware]
        session['id'] = session.id
        idconsumer = consumer.Consumer(session, self.store)
        session.save()
        return idconsumer

    def _quoteattr(self, s):
        if s == None:
            s = ''
        qs = cgi.escape(s, 1)
        return '"%s"' % (qs,)
            

class OpenIDUserSetter(AuthKitUserSetter):
    def __init__(self, app, **options):
        app = AuthOpenIDHandler(
            app,
            store_type=options['store_type'], 
            store_config = options['store_config'],
            baseurl=options.get('baseurl',''),
            path_signedin=options['path_signedin'],
            path_process=options.get('path_process','/process'),
            template = options['template'],
            urltouser = options['urltouser'],
            charset = options['charset'],
            sreg_required=options['sreg_required'],
            sreg_optional=options['sreg_optional'],
            sreg_policyurl=options['sreg_policyurl'],
        )

        if options['session_middleware'] == 'beaker.session':
            app = SessionMiddleware(
                app, 
                key=options['session_key'], 
                secret=options['session_secret']
            )
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


def load_openid_config(
    app,
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.openid', 
):
    global template
    template_ = template
    template_conf = strip_base(auth_conf, 'template.')
    if template_conf:
        template_ = get_template(template_conf, prefix=prefix+'template.')
    urltouser = auth_conf.get('urltouser', None)
    if isinstance(urltouser, str):
        urltouser = eval_import(urltouser)
    for option in ['store.type', 'store.config', 'path.signedin']:
        if not auth_conf.has_key(option):
            raise AuthKitConfigError(
                'Missing the config key %s%s'%(prefix, option)
            )
    user_setter_params={
        'store_type': auth_conf['store.type'], 
        'store_config': auth_conf['store.config'],
        'baseurl': auth_conf.get('baseurl',''),
        'path_signedin': auth_conf['path.signedin'],
        'path_process': auth_conf.get('path.process','/process'),
        'template': template_,
        'urltouser': urltouser,
        'charset': auth_conf.get('charset'),
        'sreg_required': auth_conf.get('sreg.required'),
        'sreg_optional': auth_conf.get('sreg.optional'),
        'sreg_policyurl': auth_conf.get('sreg.policyurl'),
        # XXX This need to actually be configurable, not hard coded
        'session_secret': 'asdasd',
        'session_key': 'authkit_openid',
        'session_middleware': 'beaker.session',
    }
    if user_setter_params['session_middleware'] == 'beaker.session':
        if not user_setter_params['session_secret']:
            raise AuthKitConfigError('No session_secret set')
    auth_handler_params={
        'template':user_setter_params['template'],
        'path_verify':auth_conf.get('path.verify', '/verify'),
        'baseurl':user_setter_params['baseurl'],
        'charset':user_setter_params['charset'],
    }
    return app, auth_handler_params, user_setter_params
    
def make_passurl_handler(
    app,
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.openid', 
):
    app, auth_handler_params, user_setter_params = load_openid_config(
        app,
        auth_conf, 
        app_conf=None,
        global_conf=None,
        prefix='authkit.openid', 
    )
    # Note, the session middleware should already be setup by now
    # if we are not using beaker
    app = MultiHandler(app)
    app.add_method(
        'openid', 
        OpenIDAuthHandler,
        template=auth_handler_params['template'],
        path_verify=auth_handler_params['path_verify'],
        baseurl=auth_handler_params['baseurl'],
        charset = auth_handler_params['charset'],
    )
    app.add_checker('openid', status_checker)
    # XXX Some of this functionality should be moved into OpenIDAuthHandler
    app = OpenIDUserSetter(
        app,
        **user_setter_params
    )
    return app

# Backwards compatibility
PassURLSignIn = OpenIDAuthHandler
