# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from authkit.users import sqlalchemy_driver
from paste.util.import_string import eval_import
from authkit.permissions import RequestPermission
from authkit.authorize import NotAuthorizedError
from authkit.authorize import PermissionError, NotAuthenticatedError

class AuthKitDatabaseUsers(sqlalchemy_driver.UsersFromDatabase):
    """
     Implementación de interface authkit.users.Users.
     Asume que estan definidas en el modulo ``model`` las clases User, Group,
     Role y UserRole tal como las espera sqlalchemy_driver.UsersFromDatabase
    """
    def __init__(self, model, encrypt=None):
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt
        if isinstance(model, (str, unicode)):
            model = eval_import(model)

        self.model = model

    # Existence Methods
    def user_exists(self, username):
        """
        Overrides sqlalchemy_driver.UsersFromDabase.user_exists which assumes
        that usernames are lowercase in the database. This implementation
        does not.

        Returns ``True`` if a user exists with the given username, ``False``
        otherwise. Usernames are case insensitive.
    
        FIXME Hacer que los usernames sean case insensitive
        """
        return self._getUser(username) is not None


    # User Methods
    def user_has_password(self, username, password):
        """
        Returns ``True`` if the user has the password specified, ``False``
        otherwise. Passwords are case sensitive. Raises an exception if the
        user doesn't exist.

        FIXME Hacer que los usernames sean case insensitive
        """
        user = self._getUser(username)
        if user is None:
            raise AuthKitNoSuchUserError("No such user %r"%username)

        if user.password == self.encrypt(password):
            return True
        return False

    def _getUser(self, username):
        return self.model.User.query.from_statement("""
                    select * 
                    from users 
                    where username = :username""") \
                .params(username=username).first()


class UserInRoute(RequestPermission):
    """ 
    Chequea el valor de cierto key
    en el diccionario armado por routes 
    """
    def __init__(self, usernameKey):
        self.key = usernameKey

    def check(self, app, environ, start_response):
        if 'pylons.routes_dict' not in environ:
            # TODO: mandar un error acorde
            raise NotAuthorizedError('No routes dict')
        
        
        routesDict = environ['pylons.routes_dict']
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')

        #print "routes: " + routesDict[self.key]
        #print "environ: " + environ['REMOTE_USER']

        if self.key not in routesDict or \
                routesDict[self.key] != environ['REMOTE_USER']:
            raise NotAuthorizedError('Not Authorized')

        return app(environ, start_response)
        


