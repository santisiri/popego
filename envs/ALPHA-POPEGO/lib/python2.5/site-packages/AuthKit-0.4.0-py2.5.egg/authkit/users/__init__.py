"""Objects representing users, their passwords, roles and groups

The objects defined in this file used in conjunction with authentication,
authorization and permission objects form a complete user management system.

However, there is no requirement to use this user management API at all. If you
define your own authentication checks by specifying your own
``valid_password()`` or ``digest_password()`` methods when setting up the
authentication middleware, and you create your own permissions objects based on
your own requriements then you will have no need for this implementation. It is
simply provided as a useful default implementation for users looking for a
simple, ready made solution that doesn't require any integration. 

The implementation consists of the following:

``authkit.authenticate.valid_password()``
    A ``valid_password()`` implementation used by default with the
    ``basic`` or ``form`` authentication methods that checks usernames and
    passwords against those defined in the user management API object.
 
``authkit.authenticate.digest_password()``
    A ``digest_password()`` implementation used by default with the
    ``digest`` authentication which produces a digest from the users set up
    in the user management API object.

``authkit.permissions.HasAuthKitRole``
    A permission object which checks the signed in user's role from the 
    user management API object.

``authkit.permissions.HasAuthKitGroup``
    A permission object which checks the signed in user's group from the 
    user management API object.

``authkit.permissions.ValidAuthKitUser``
    A permission object which checks the signed in user is defined in the 
    user management API object.

Of course since the user management API is fairly generic, it is possible to
have different implementations. This module has two implementations both
derived from the base ``Users`` class. They are ``UsersFromString`` and
``UsersFromFile``. By default, ``authkit.authenticate.middleware`` uses
``UsersFromString`` and expects you to specify your users, groups and roles as
a string in the config file in the way described in the main AuthKit manual but
you can also specify you wish to use the alternative implementation to load
your user data from a file.

Of course you are also free to create your own implementation derived from
``Users`` and as long as it keeps the same API, the existing functions and
permissions mentioned earlier will work without modification when using your
user management API object. This means that if your requirements are very
simple you might prefer to create a custom ``Users`` object rather than
integrate AuthKit into your project in the slightly lower level fashion by
defining the ``valid_password()`` and ``digest_password()`` functions and any
necessary permissions.

If you are using the authentication middleware with users, the ``Users`` object
will be available in your code as ``environ[authkit.users]``.  
"""

import os.path
import md5 as _md5
from authkit.authenticate import AuthKitConfigError

#
# Encryption Functions
#

def md5(password, secret=''):
    result = _md5.md5(password)
    result.update(secret)
    return result.hexdigest()

#
# Exceptions
#

class AuthKitNoSuchUserError(Exception):
    pass
    
class AuthKitNoSuchRoleError(Exception):
    pass

class AuthKitNoSuchGroupError(Exception):
    pass
    
class AuthKitNotSupportedError(Exception):
    pass

class AuthKitError(Exception):
    pass
    
#
# Users classes
#

class Users(object):
    """
    Base class from which all other Users classes should be derived.
    """
    def __init__(self, data, encrypt=None):
        self.data = data
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt

    # Create Methods
    def user_create(self, username, password, group=None):
        """
        Create a new user with the username, password and group name specified.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    def role_create(self, role):
        """
        Add a new role to the system
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    def group_create(self, group):
        """
        Add a new group to the system
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    # Delete Methods
    def user_delete(self, username):
        """
        Remove the user with the specified username 
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def role_delete(self, role):
        """
        Remove the role specified. Rasies an exception if the role is still in use. 
        To delete the role and remove it from all existing users use ``role_delete_cascade()``
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def group_delete(self, group):
        """
        Remove the group specified. Rasies an exception if the group is still in use. 
        To delete the group and remove it from all existing users use ``group_delete_cascade()``
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    # Delete Cascade Methods
    def role_delete_cascade(self, role):
        """
        Remove the role specified and remove the role from any users who used it
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def group_delete_cascade(self, group):
        """
        Remove the group specified and remove the group from any users who used it
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    # Existence Methods
    def user_exists(self, username):
        """
        Returns ``True`` if a user exists with the given username, ``False`` otherwise. Usernames are case insensitive.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are case insensitive.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def group_exists(self, group):
        """
        Returns ``True`` if the group exists, ``False`` otherwise. Groups are case insensitive.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    # List Methods
    def list_roles(self):
        """
        Returns a lowercase list of all role names ordered alphabetically
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def list_users(self):
        """
        Returns a lowecase list of all usernames ordered alphabetically
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def list_groups(self):
        """
        Returns a lowercase list of all groups ordered alphabetically
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    # User Methods
    def user(self, username):
        """
        Returns a dictionary in the following format:

        .. code-block :: Python
        
            {
                'username': username,
                'group':    group,
                'password': password,
                'roles':    [role1,role2,role3... etc]
            }

        The role names are ordered alphabetically
        Raises an exception if the user doesn't exist.
        """    
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_roles(self, username):
        """
        Returns a list of all the role names for the given username ordered alphabetically. Raises an exception if
        the username doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_group(self, username):
        """
        Returns the group associated with the user or ``None`` if no group is associated.
        Raises an exception is the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_password(self, username):
        """
        Returns the password associated with the user or ``None`` if no password exists.
        Raises an exception is the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` otherwise. Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_has_group(self, username, group):
        """
        Returns ``True`` if the user has the group specified, ``False`` otherwise. The value for ``group`` can be ``None`` to test that the user doesn't belong to a group. Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    def user_has_password(self, username, password):
        """
        Returns ``True`` if the user has the password specified, ``False`` otherwise. Passwords are case sensitive.
        Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    def user_set_username(self, username, new_username):
        """
        Sets the user's username to the lowercase of new_username. 
        Raises an exception if the user doesn't exist or if there is already a user with the username specified by ``new_username``.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_set_group(self, username, group, add_if_necessary=False):
        """
        Sets the user's group to the lowercase of ``group`` or ``None``. If the group doesn't exist and ``add_if_necessary`` is ``True`` the group will also be added. Otherwise an ``AuthKitNoSuchGroupError`` will be raised.
        Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_add_role(self, username, role, add_if_necessary=False):
        """
        Sets the user's role to the lowercase of ``role``. If the role doesn't exist and ``add_if_necessary`` is ``True`` the role will also be added. Otherwise an ``AuthKitNoSuchRoleError`` will be raised.
        Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
    def user_remove_role(self, username, role):
        """
        Removes the role from the user specified by ``username``. Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )

    def user_remove_group(self, username):
        """
        Sets the group to ``None`` for the user specified by ``username``. Raises an exception if the user doesn't exist.
        """
        raise AuthKitNotSupportedError(
            "The %s implementation of the User Management API doesn't support this method"%(
                self.__class__.__name__
            )
        )
        
class UsersReadOnly(Users):
    """
    Like the ``Users`` class except that user information is read only. All the information
    is obtained from the attributes self.usernames, self.passwords, self.roles, self.groups
    which are expected to be setup in ``__init__()``.
    
    ``usernames`` should be a list of lowercase usernames
    ``passwords``, ``groups`` should be a dictionary where the keys are lowercase usernames
    and the values are the corresponding lowercase group name or password.
    ``roles`` is similar to ``passwords`` and ``groups`` except values are lists of lowercase role names.
    """

    # Existence Methods
    def user_exists(self, username):
        """
        Returns ``True`` if a user exists with the given username, ``False`` otherwise. Usernames are case insensitive.
        """
        return username.lower() in self.list_users()
        
    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are case insensitive.
        """
        return role.lower() in self.list_roles()
        
    def group_exists(self, group):
        """
        Returns ``True`` if the group exists, ``False`` otherwise. Groups are case insensitive.
        """
        return group.lower() in self.list_groups()
        
    # List Methods
    def list_roles(self):
        """
        Returns a lowercase list of all role names ordered alphabetically
        """
        roles = []
        for k,v in self.roles.items():
            for role in v:
                role_ = role.lower()
                if role_ and role_ not in roles:
                    roles.append(role_)
        roles.sort()
        return roles
        
    def list_users(self):
        """
        Returns a lowecase list of all usernames ordered alphabetically
        """
        # Return a copy in case someone starts modifying it.
        return [u for u in self.usernames]

    def list_groups(self):
        """
        Returns a lowercase list of all groups ordered alphabetically
        """
        groups = []
        for k,v in self.groups.items():
            if v and v not in groups:
                groups.append(v)
        groups.sort()
        return groups

    # User Methods
    def user(self, username):
        """
        Returns a dictionary in the following format:

        .. code-block :: Python
        
            {
                'username': username,
                'group':    group,
                'password': password,
                'roles':    [role1,role2,role3... etc]
            }

        The role names are ordered alphabetically
        Raises an exception if the user doesn't exist.
        """    
        username = username.lower()
        if not username in self.usernames:
            raise AuthKitNoSuchUserError("No user named %r"%username)
        else:
            return {
                'username': username,
                'group':    self.user_group(username),
                'password': self.user_password(username),
                'roles':    self.user_roles(username),
            }
        
    def user_roles(self, username):
        """
        Returns a list of all the role names for the given username ordered alphabetically. Raises an exception if
        the username doesn't exist.
        """
        username = username.lower()
        if not username in self.usernames:
            raise AuthKitNoSuchUserError("No user named %r"%username)
        return self.roles[username]
        
    def user_group(self, username):
        """
        Returns the group associated with the user or ``None`` if no group is associated.
        Raises an exception is the user doesn't exist.
        """
        username = username.lower()
        if not username in self.usernames:
            raise AuthKitNoSuchUserError("No user named %r"%username)
        return self.groups[username]

    def user_password(self, username):
        """
        Returns the password associated with the user or ``None`` if no password exists.
        Raises an exception is the user doesn't exist.
        """
        username = username.lower()
        if not username in self.usernames:
            raise AuthKitNoSuchUserError("No user named %r"%username)
        return self.passwords[username]
        
    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` otherwise. Raises an exception if the user doesn't exist.
        """
        return role.lower() in self.user_roles(username)
        
    def user_has_group(self, username, group):
        """
        Returns ``True`` if the user has the group specified, ``False`` otherwise. Raises an exception if the user doesn't exist.
        """
        return group.lower() == self.user_group(username.lower())

    def user_has_password(self, username, password):
        """
        Passwords are case sensitive.
        Returns ``True`` if the user has the password specified, ``False`` otherwise. 
        Raises an exception if the user doesn't exist.
        """
        return self.encrypt(password) == self.user_password(username.lower())
        
def parse(data):
    """
    Parses the user data
    """
    passwords = {}
    roles = {}
    groups = {}
    counter = 1
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        role_list = []
        parts = line.split(' ')
        if len(parts) > 1:
            for role in parts[1:]:
                if role:
                    role_list.append(role.strip().lower())
        role_list.sort()
        group = None
        parts = parts[0].split(':')
        if len(parts) > 1:
            password = parts[1]
            if not password:
                'Password for %s is empty'%(
                    username,
                )
            username = parts[0].lower()
            if not username:
                'Username on line %s is empty'%(
                    counter,
                )
        if len(parts) == 3:
            group = parts[2].lower()
        if len(parts) <= 1 or len(parts) > 3:
            raise AuthKitConfigError(
                'Syntax error on line %s of authenticate list'%(
                    counter,
                )
            )
        if passwords.has_key(username):
            raise AuthKitConfigError(
                'Username %r defined twice in authenticate list %r'%(
                    username,
                    passwords
                )
            )
        else:
            passwords[username] = password
        if role_list:
            roles[username] = role_list
        if group:
            groups[username] = group
        counter += 1
    usernames = passwords.keys()
    usernames.sort()
    for username in usernames:
        if not passwords.has_key(username):
            raise AuthKitError('No password specified for user %r'%username)
        if not roles.has_key(username):
            roles[username] = []
        if not groups.has_key(username):
            groups[username] = None
    assert len(usernames) == len(passwords) == len(roles) == len(groups)
    return usernames, passwords, roles, groups

class UsersFromString(UsersReadOnly):
    """
    A ``Users`` class which cbtains user information from a string with lines
    formatted as` ``username1:password1:group role1, role2 etc`` where 
    ``group`` is optional and zero or more roles can exist. 

    One set of user information should be on each line and extra whitespace is
    stripped.  """ 
    def __init__(self, data, encrypt=None):
        self.usernames, self.passwords, self.roles, self.groups = parse(data)
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt
    
class UsersFromFile(UsersReadOnly):
    """
    A Users class with the same implementation as ``UsersFromString`` except that
    user information is obtained from a file. The file should contain user information
    in the same format as the string accepted for ``UsersFromString``.
    """
    def __init__(self, filename, encrypt=None):
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt
        string = None
        fp = None
        try:
            if not os.path.exists(filename) and os.path.isfile(filename):
                raise AuthKitError('File does not exist %r'%filename)
            fp = open(filename, 'r')
            string = fp.read()
        finally:
            if fp:
                fp.close()
        self.usernames, self.passwords, self.roles, self.groups = parse(string)

