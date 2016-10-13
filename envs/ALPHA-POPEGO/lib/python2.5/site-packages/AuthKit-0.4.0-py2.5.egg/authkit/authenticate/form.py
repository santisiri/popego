"""Form and cookie based authentication middleware

As with all the other AuthKit middleware, this middleware is described in
detail in the AuthKit manual and should be used via the
``authkit.authenticate.middleware`` function.

The option form.status can be set to "200 OK" if the Pylons error document
middleware is intercepting the 401 response and just showing the standard 401
error document. This will not happen in recent versions of Pylons (0.9.6)
because this middleware sets the environ['pylons.error_call'] key so that the
error documents middleware doesn't intercept the response.
"""

from paste.auth.form import AuthFormHandler
from paste.request import construct_url, parse_formvars
from authkit.authenticate import get_template, valid_password, \
   get_authenticate_function, strip_base, RequireEnvironKey, \
   AuthKitAuthHandler
from authkit.authenticate.multi import MultiHandler, status_checker

import logging
log = logging.getLogger('authkit.authenticate.form')

def template():
    return """\
<html>
  <head><title>Please Sign In</title></head>
  <body>
    <h1>Please Sign In</h1>
    <form action="%s" method="post">
      <dl>
        <dt>Username:</dt>
        <dd><input type="text" name="username"></dd>
        <dt>Password:</dt>
        <dd><input type="password" name="password"></dd>
      </dl>
      <input type="submit" name="authform" value="Sign In" />
    </form>
  </body>
</html>
"""

class FormAuthHandler(AuthKitAuthHandler, AuthFormHandler):
    def __init__(
        self, 
        app,
        charset=None,
        status="401 Unauthorized",
        **p
    ):
        AuthFormHandler.__init__(self, app, **p)
        self.status = status
        if charset is None:
            self.charset = ''
        else:
            self.charset = '; charset='+charset
    
    def on_authorized(self, environ, start_response):
        environ['paste.auth_tkt.set_user'](userid=environ['REMOTE_USER'])
        return self.application(environ, start_response)
        
    def __call__(self, environ, start_response):
        # Shouldn't ever allow a response if this is called via the 
        # multi handler
        username = environ.get('REMOTE_USER','')
        if 'POST' == environ['REQUEST_METHOD']:
            formvars = parse_formvars(environ, include_get_vars=False)
            username = formvars.get('username')
            password = formvars.get('password')
            if username and password:
                if self.authfunc(environ, username, password):
                    environ['AUTH_TYPE'] = 'form'
                    environ['REMOTE_USER'] = username
                    environ['REQUEST_METHOD'] = 'GET'
                    environ['CONTENT_LENGTH'] = ''
                    environ['CONTENT_TYPE'] = ''
                    del environ['paste.parsed_formvars']
                    return self.on_authorized(environ, start_response)
        action =  construct_url(environ)
        log.debug("Form action is: %s", action)
        content = self.template() % action
        # @@@ Tell Pylons error documents middleware not to intercept the 
        # response
        environ['pylons.error_call'] = 'authkit'
        start_response(self.status,[('Content-Type', 'text/html'+self.charset),
                                 ('Content-Length', str(len(content)))])
        return [content]

def load_form_config(
    app, 
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.method.form',
):
    app = RequireEnvironKey(
        app,
        'paste.auth_tkt.set_user',
        missing_error=(
            'Missing the key %(key)s from the environ. '
            'Have you added the cookie method after the form method?'
        )
    )
    template_conf = strip_base(auth_conf, 'template.')
    if template_conf:
        template_ = get_template(template_conf, prefix=prefix+'template.')
    else:
        template_ = template
    authenticate_conf = strip_base(auth_conf, 'authenticate.')
    app, authfunc, users = get_authenticate_function(
        app, 
        authenticate_conf, 
        prefix=prefix+'authenticate.', 
        format='basic'
    )
    charset=auth_conf.get('charset')
    return app, {'authfunc':authfunc, 'template':template_, 'charset':charset}, None

def make_form_handler(
    app, 
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.method.form', 
):
    app, auth_handler_params, user_setter_params = load_form_config(
        app, 
        auth_conf, 
        app_conf=None,
        global_conf=None,
        prefix='authkit.method.form',
    )
    app = MultiHandler(app)
    app.add_method(
        'form', 
        FormAuthHandler, 
        authfunc=auth_handler_params['authfunc'], 
        template=auth_handler_params['template'], 
        charset=auth_handler_params['charset']
    )
    app.add_checker('form', status_checker)
    return app

# Backwards compatbility
Form = FormAuthHandler

