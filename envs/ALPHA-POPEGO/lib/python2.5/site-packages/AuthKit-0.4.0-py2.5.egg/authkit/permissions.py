"""Permission objects

Permission objects are used to define which users should have access to a particular
resource. They are checked using some of the authorization objects either in the
``authkit.authorize`` module or ``authkit.pylons_adaptors`` module if you are using
Pylons.

Permissions objects are very similar to WSGI applications and can perform a
check based on the request or the response. Not all of the authorization
objects have access to the response because the permission might be checked as
part of a code block before the response is generated. This leads to two
classes of permissions, request-based (which can be checked anywhere) and
responce-based which can only be checked when the authorization object has
access to the response. 

All the built-in AuthKit permissions are request-based but you can use the
permissions objects defined in this module or create your own derived from
``authkit.permission.Permission``.

Permissions are described in detail in the AuthKit manual.
"""

from authkit.authorize import PermissionError, NotAuthenticatedError
from authkit.authorize import NotAuthorizedError, middleware

import datetime
import logging
log = logging.getLogger('authkit.permissions')

class AuthKitConfigError(Exception): 
    """
    Raised when there is a problem with the
    configuration options chosen for the authenticate middleware
    """
    pass
    
no_authkit_users_in_environ = AuthKitConfigError(
    'No authkit.users object exists in the environment. You may have '
    'forgotton to specify a Users object or are using the the default '
    'valid_password() method in the authenticate middleware when you '
    'may have meant to specify your own.'
)

# 
# Permission Classes
#

class Permission(object):
    """
    The base class for all permissions objects. 

    The ``check()`` method is called by the authorization object to check the
    permission. Permissions should return the original status, headers and
    response or raise a ``NotAuthorizedError`` when their ``check()`` method is
    called. 

    .. Note ::
    
        The WSGI ``app`` can only be called once by the ``check()`` method.
        This means that you cannot write permisisons objects that perform
        logical ``not`` and ``or`` operations on other permissions objects
        since doing so might require the same app to be called multiple times.
        A permission object to perform an ``and`` operation is feasible and has
        been impleneted as the ``And`` permission class.  
        
   """

    def check(self, app, environ, start_response): 
        return app(environ, start_response)

class RequestPermission(Permission):
    """
    The base class for all request-based permissions
    """
    pass

class _TestBadlyLabelledResponseBasedPermission(RequestPermission):
    def check(self, app, environ, start_response):
        def start_response(a,b,c=None):
            return start_response(a,b,c)
        return app(environ, start_response)
        
class UserIn(RequestPermission):
    """
    Checks the ``REMOTE_USER`` is one of the users specified.
    
    Takes the following arguments:

    ``users``
        A list of usernames which are valid

    If there is no ``REMOTE_USER`` a ``NotAuthenticatedError`` is raised. If
    the ``REMOTE_USER`` is not in ``users`` a ``NotAuthorizedError`` is raised.

    Usernames supplied to ``users`` are treated case insensitively.
    """

    def __init__(self, users):
        if isinstance(users, list) or isinstance(users, tuple):
            users_ = []
            for user in users:
                users_.append(user.lower())
            self.users = users_
        elif isinstance(users, str):
            self.users = [users]
        else:
            raise PermissionSetupError('Expected users to be a list or a string, not %r'%users)
      
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        if environ['REMOTE_USER'] not in self.users:
            raise NotAuthorizedError('You are not one of the users allowed to access this resource.')
        return app(environ, start_response)

class Exists(RequestPermission):
    """
    Checks the specified key is present in the ``environ``.
    
    Takes the following arguments:

    ``key``
        The required key

    ``error``
        The error to be raised if the key is missing. XXX This argument may be deprecated soon.

    """

    def __init__(self, key, error=NotAuthorizedError('Not Authorized')):
        self.key = key
        self.error = error
    
    def check(self, app, environ, start_response):
        if self.key not in environ:
            raise self.error
        return app(environ, start_response)
        
class And(RequestPermission):
    """
    Checks all the permission objects listed as keyword arguments in turn.
    Permissions are checked from left to right. The error raised by the ``And``
    permission is the error raised by the first permission check to fail.
    """

    def __init__(self, *permissions):
        if len(permissions) < 2:
            raise PermissionSetupError('Expected at least 2 permissions objects')
        permissions = list(permissions)
        permissions.reverse()
        self.permissions = permissions
        
    def check(self, app, environ, start_response):
        for permission in self.permissions:
            app = middleware(app, permission)
        #raise Exception(app, self.permissions)
        return app(environ, start_response)

class RemoteUser(RequestPermission):
    """
    Checks someone is signed in by checking for the presence of the
    ``REMOTE_USER``.
    
    If ``accept_empty`` is ``False`` (the default) then an empty ``REMOTE_USER``
    will not be accepted and the value of ``REMOTE_USER`` must evaluate to 
    ``True`` in Python.
    """

    def __init__(self, accept_empty=False):
        self.accept_empty = accept_empty

    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        elif self.accept_empty==False and not environ['REMOTE_USER']:
            raise NotAuthorizedError('Not Authorized')
        return app(environ, start_response)

#
# Permissions to work with the AuthKit user management API
#

class HasAuthKitRole(RequestPermission):
    """
    Designed to work with the user management API described in the AuthKit manual.

    This permission checks that the signed in user has any if the roles specified
    in ``roles``. If ``all`` is ``True``, the user must have all the roles for
    the permission check to pass.
    """

    def __init__(self, roles, all=False, error=None):
        if isinstance(roles, str):
            roles = [roles]
        self.all = all
        self.roles = roles
        self.error = error
        
    def check(self, app, environ, start_response):
        """
        Should return True if the user has the role or
        False if the user doesn't exist or doesn't have the role.

        In this implementation role names are case insensitive.
        """
        
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        if not environ.get('REMOTE_USER'):
            if self.error:
                raise self.error
            raise NotAuthenticatedError('Not authenticated')
        
        users = environ['authkit.users']
        if not users.user_exists(environ['REMOTE_USER']):
            raise NotAuthorizedError('No such user')
        # Check the groups specified when setup actually exist
        for role in self.roles:
            if not users.role_exists(role):
                raise Exception("No such role %r exists"%role)
        if self.all:
            for role in self.roles:
                if not users.user_has_role(environ['REMOTE_USER'], role):
                    if self.error:
                        raise self.error
                    else:
                        raise NotAuthorizedError(
                            "User doesn't have the role %s"%role.lower()
                        )
            return app(environ, start_response)
        else:
            for role in self.roles:
                if users.user_has_role(environ['REMOTE_USER'], role):
                    return app(environ, start_response)
            if self.error:
                raise self.error
            else:
                raise NotAuthorizedError(
                    "User doesn't have any of the specified roles"
                )
    
class HasAuthKitGroup(RequestPermission):
    """
    Designed to work with the user management API described in the AuthKit manual.

    This permission checks that the signed in user is in one of the groups specified
    in ``groups``.
    """

    def __init__(self, groups, error=None):
        if isinstance(groups, str):
            groups = [groups]
        self.groups = groups
        self.error = error
        
    def check(self, app, environ, start_response):
        """
        Should return True if the user has the group or
        False if the user doesn't exist or doesn't have the group.

        In this implementation group names are case insensitive.
        """
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        if not environ.get('REMOTE_USER'):
            if self.error: 
                raise self.error
            raise NotAuthenticatedError('Not authenticated')
        users = environ['authkit.users']
        # Check the groups specified when setup actually exist
        for group in self.groups:
            if group is not None:
                if not users.group_exists(group):
                    raise Exception("No such group %r exists"%group)
        
        if not users.user_exists(environ['REMOTE_USER']):
            raise NotAuthorizedError('No such user')
        for group in self.groups:
            if users.user_has_group(environ['REMOTE_USER'], group):
                return app(environ, start_response)
        if self.error:
            raise self.error
        else:
            raise NotAuthorizedError(
                "User is not a member of the specified group(s) %r"%self.groups
            )

class ValidAuthKitUser(UserIn):
    """
    Checks that the signed in user is one of the users specified when setting up
    the user management API.
    """
    def __init__(self):
        pass
    
    def check(self, app, environ, start_response):
        if 'authkit.users' not in environ:
            raise no_authkit_users_in_environ
        if not environ.get('REMOTE_USER'):
            raise NotAuthenticatedError('Not Authenticated')
        if not environ['authkit.users'].user_exists(environ['REMOTE_USER']):
            raise NotAuthorizedError(
                'You are not one of the users allowed to access this resource.'
            )
        return app(environ, start_response)

class FromIP(RequestPermission):
    """
    Checks that the remote host specified in the environment ``key`` is one 
    of the hosts specified in ``hosts``.
    """
    def __init__(self, hosts, key='REMOTE_ADDR'):
        self.hosts = hosts
        if not isinstance(self.hosts, (list, tuple)):
            self.hosts = [hosts]
        self.key = key
        
    def check(self, app, environ, start_response):
        if self.key not in environ:
            raise Exception(
                "No such key %r in environ so cannot check the host"%self.key
            )
        if not environ.get(self.key) in self.hosts:
            raise NotAuthorizedError('Host %r not allowed'%environ.get(self.key))
        return app(environ, start_response)

class BetweenTimes(RequestPermission):
    """
    Only grants access if the request is made on or after ``start`` and 
    before ``end``. Times should be specified as datetime.time objects.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def check(self, app, environ, start_response):
        today = datetime.datetime.now()
        now = datetime.time(today.hour, today.minute, today.second, today.microsecond)
        error = NotAuthorizedError("Not authorized at this time of day")
        if self.end > self.start:
            if now >= self.start and now < self.end:
                return app(environ, start_response)
            else:
                raise error
        else:
            if now < datetime.time(23, 59, 59, 999999) and now >= self.start:
                return app(environ, start_response)
            elif now >= datetime.time(0) and now < self.end:
                return app(environ, start_response)
            else:
                raise error
