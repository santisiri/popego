"""Internal forward middleware for manual authentication handling

For an example of the use of this middleware read the main AuthKit manual or
look at the Pylons example at http://pylonshq.com/project/pylonshq/wiki/PylonsWithAuthKitForward
"""

from paste.recursive import RecursiveMiddleware, ForwardRequestException, \
   CheckForRecursionMiddleware
from authkit.authenticate.multi import MultiHandler, status_checker
from authkit.authenticate import AuthKitConfigError

class Redirect(object):
    def __init__(self, app, forward_signin):
        self.app = app
        self.signin_path = forward_signin

    def __call__(self, environ, start_response):
        raise ForwardRequestException(self.signin_path)

class MyRecursive(object):
    def __init__(self, app):
        self.application = app
    def __call__(self, environ, start_response):
        try:
            result = []
            app_iter = self.application(environ, start_response)
            for data in app_iter:
                result.append(data)
            if hasattr(app_iter, 'close'):
                app_iter.close()
            return result
        except ForwardRequestException, e:
            return CheckForRecursionMiddleware(e.factory(self), environ)(environ, start_response)


def make_forward_handler(
    app,
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.forward', 
):
    if not auth_conf.has_key('internalpath'):
        raise AuthKitConfigError("No %sinternalpath key specified"%prefix)
    app = MultiHandler(app)
    app.add_method(
        'forward', 
        Redirect,  
        auth_conf['internalpath']
    )
    app.add_checker('forward', status_checker)
    app = MyRecursive(RecursiveMiddleware(app))
    return app

