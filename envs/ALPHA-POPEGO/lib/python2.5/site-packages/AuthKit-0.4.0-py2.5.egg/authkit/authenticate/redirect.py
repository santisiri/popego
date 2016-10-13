"""\
Redirect middleware to redirect the browser to a different URL for sign in
"""
from authkit.authenticate import middleware
from authkit.authenticate.multi import MultiHandler, status_checker

class HandleRedirect(object):
    def __init__(self, app, redirect_to):
        self.app = app
        self.redirect_to = redirect_to

    def __call__(self, environ, start_response):
        start_response('302 Found', [
            ('Location',self.redirect_to),
            ('Content-Type','text/plain'),
            ('Content-Length','0'),
        ])
        return ['redirecting to %s'%self.redirect_to]

def make_redirect_handler(
    app, 
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.method.redirect.', 
):
    app = MultiHandler(app)
    app.add_method('redirect', HandleRedirect, redirect_to = auth_conf['url'])
    app.add_checker('redirect', status_checker)
    return app

