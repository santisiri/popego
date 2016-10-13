"""Pylons specific code to facilitate using AuthKit with Pylons

There is a full Pylons manual in addition to the AuthKit manual which 
you should read if you plan to use AuthKit with Pylons

.. Note ::

    In addition to the authorize methods described here, you can also use the
    default ``authkit.authorize.middleware`` function to add WSGI middleware
    authorization checks to your Pylons application since Pylons has a full
    WSGI middleware stack. Just add the middleware to your project's
    ``config/middleware.py`` file.

"""

from decorator import decorator
from pylons import request

from authkit.authorize import PermissionSetupError
from authkit.authorize import NotAuthenticatedError, NotAuthorizedError
from authkit.authorize import authorize_request as authkit_authorize_request

def authorize(permission):
    """
    This is a decorator which can be used to decorate a Pylons controller action.
    It takes the permission to check as the only argument and can be used with
    all types of permission objects.
    """
    def validate(func, self, *args, **kwargs):
        def app(environ, start_response):
            return func(self, *args, **kwargs)
        return permission.check(app, request.environ, self.start_response)
    return decorator(validate)

def authorize_request(permission):
    """
    This function can be used within a controller action to ensure that no code 
    after the function call is executed if the user doesn't pass the permission
    check specified by ``permission``.

    .. Note ::

        Unlike the ``authorize()`` decorator or
        ``authkit.authorize.middleware`` middleware, this function has no
        access to the WSGI response so cannot be used to check response-based
        permissions.  Since almost all AuthKit permissions are request-based
        this shouldn't be a big problem unless you are defining your own 
        advanced permission checks.
    """
    authkit_authorize_request(request.environ, permission)

def authorized(permission):
    """
    Similar to the ``authorize_request()`` function with no access to the
    request but rather than raising an exception to stop the request if a
    permission check fails, this function simply returns ``False`` so that you
    can test permissions in your code without triggering a sign in. It can
    therefore be used in a controller action or template.

    Use like this::

        if authorized(permission):
            return Response('You are authorized')
        else:
            return Response('Access denied')
 
    """
    try:
        authorize_request(permission)
    except (NotAuthorizedError, NotAuthenticatedError):
        return False
    else:
        return True

