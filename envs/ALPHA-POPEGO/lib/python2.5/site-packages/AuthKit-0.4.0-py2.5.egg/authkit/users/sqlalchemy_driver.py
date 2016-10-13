from sqlalchemy.ext.assignmapper import assign_mapper
from sqlalchemy import *
from paste.util.import_string import eval_import
from authkit.users import *

class UsersFromDatabase(Users):
    """
    Database Version
    """
    def __init__(self, model, encrypt=None):
        if encrypt is None:
            def encrypt(password):
                return password
        self.encrypt = encrypt
        if isinstance(model, (str, unicode)):
            model = eval_import(model)
            
        if hasattr(model, 'authkit_initialized'):
            raise AuthKitError(
                'The AuthKit database model has already been setup'
            )
        else:
            model.authkit_initialized = True


        self.model = self.update_model(model)
        
    def update_model(self, model):
        
        meta = model.meta
        ctx = model.ctx
        
        class User(object):
            def __init__(
                self,
                username,
                uid=None,
                password=None,
                group_uid=None,
            ):
                self.id         = id
                self.username   = username
                self.password   = password
                self.group_uid  = group_uid
            def __repr__(self):
                return "User(%(username)s)" % self.__dict__

        class Group(object):
            def __init__(self, name=None):
                self.name = name
            def __repr__(self):
                return "Group(%(name)s)" % self.__dict__
                
        class Role(object):
            def __init__(self, name=None):
                self.name = name
            def __repr__(self):
                return "Role(%(name)s)" % self.__dict__
                
        # Tables
        groups_table = Table(
            "groups",
            meta,
            Column("uid",        Integer,        primary_key=True),
            Column("name",      String(255),    unique=True,    nullable=False),
        )
        roles_table = Table(
            "roles",
            meta,
            Column("uid",        Integer,        primary_key=True),
            Column("name",      String(255),    unique=True,    nullable=False),
        )
        users_table = Table(
            "users",
            meta,
            Column("uid",        Integer,        primary_key=True),
            Column("username",  String(255),    unique=True,    nullable=False),
            Column("password",  String(255),     nullable=False),
            Column("group_uid",  Integer,        ForeignKey("groups.uid")),
        )
        users_roles_table = Table(                # many:many relation table
            "users_roles",
            meta,
            Column("user_uid",   Integer,        ForeignKey("users.uid")),
            Column("role_uid",   Integer,        ForeignKey("roles.uid")),
        )
           
        groups_mapper = assign_mapper(
            ctx,
            Group,
            groups_table,
            properties={
                "users": relation(User)
            }
        )
        users_mapper = assign_mapper(
            ctx,
            User,
            users_table,
            properties={
                "roles": relation(Role, lazy=True, secondary=users_roles_table),
                "group": relation(Group),
            }
        )
        roles_mapper = assign_mapper(
            ctx,
            Role,
            roles_table,
            properties={
                "users": relation(User, lazy=True, secondary=users_roles_table)
            }
        )

        model.User = User
        model.Group = Group
        model.Role = Role
        return model
       
    # Create Methods
    def user_create(self, username, password, group=None):
        """
        Create a new user with the username, password and group name specified.
        """
        if ' ' in username:
            raise AuthKitError("Usernames cannot contain space characters")
        if self.user_exists(username):
            raise AuthKitError("User %r already exists"%username)            
        if group is None:
            new_user = self.model.User(
                username=username.lower(), 
                password=self.encrypt(password)
            )
        else:
            if not self.group_exists(group):
                raise AuthKitNoSuchGroupError(
                    "There is no such group %r"%group
                )
            new_user = self.model.User(
                username=username.lower(), 
                password=self.encrypt(password), 
                group_uid=self.model.Group.get_by(name=group.lower()).uid
            )
        new_user.flush()

    def role_create(self, role):
        """
        Add a new role to the system
        """
        if ' ' in role:
            raise AuthKitError("Roles cannot contain space characters")
        if self.role_exists(role):
            raise AuthKitError("Role %r already exists"%role)
        new_role = self.model.Role(role.lower())
        new_role.flush()
        
        #~ new_role2 = self.model.Role("test")
        #~ #new_role2.flush()
        #~ from pysqlite2 import dbapi2 as sqlite
        #~ conn = sqlite.connect("mydb.db")
        #~ cur = conn.cursor()
        #~ cur.execute("SELECT * FROM roles;")
        #~ raise Exception(cur.fetchall(), self.model.Role.get(1))
        #~ raise Exception([repr(obj) for obj in self.model.ctx.current], self.model.ctx.current.identity_map.values())
        #~ self.model.ctx.current.flush()
        #~ raise Exception([u.name for u in self.model.Role.select(order_by=self.model.Role.c.name)])
        #new_role.flush()
        
    def group_create(self, group):
        """
        Add a new group to the system
        """
        if ' ' in group:
            raise AuthKitError("Groups cannot contain space characters")
        if self.group_exists(group):
            raise AuthKitError("Group %r already exists"%group)
        new_group = self.model.Group(group.lower())
        new_group.flush()

    # Delete Methods
    def user_delete(self, username):
        """
        Remove the user with the specified username 
        """
        user = self.model.User.get_by(username=username.lower())
        if not user:
            raise AuthKitNoSuchUserError("There is no such user %r"%username)
        else:
            user.delete()
            user.flush()

    def role_delete(self, role):
        """
        Remove the role specified. Rasies an exception if the role is still in use. 
        To delete the role and remove it from all existing users use 
        ``role_delete_cascade()``
        """
        role = self.model.Role.get_by(name=role.lower())
        if not role:
            raise AuthKitNoRoleUserError("There is no such role %r"%role)
        else:
            role.delete()
            role.flush()
            
    def group_delete(self, group):
        """
        Remove the group specified. Rasies an exception if the group is still in use. 
        To delete the group and remove it from all existing users use ``group_delete_cascade()``
        """
        group = self.model.Group.get_by(name=group.lower())
        if not group:
            raise AuthKitNoGroupUserError("There is no such group %r"%group)
        else:
            group.delete()
            group.flush()
            
    #~ # Delete Cascade Methods
    #~ def role_delete_cascade(self, role):
        #~ """
        #~ Remove the role specified and remove the role from any users who used it
        #~ """
        #~ raise AuthKitNotSupportedError(
            #~ "The %s implementation of the User Management API doesn't support this method"%(
                #~ self.__class__.__name__
            #~ )
        #~ )
        
    #~ def group_delete_cascade(self, group):
        #~ """
        #~ Remove the group specified and remove the group from any users who used it
        #~ """
        #~ raise AuthKitNotSupportedError(
            #~ "The %s implementation of the User Management API doesn't support this method"%(
                #~ self.__class__.__name__
            #~ )
        #~ )
        
    # Existence Methods
    def user_exists(self, username):
        """
        Returns ``True`` if a user exists with the given username, ``False`` 
        otherwise. Usernames are case insensitive.
        """
        user = self.model.User.get_by(username=username.lower())
        if user:
            return True
        return False
        
    def role_exists(self, role):
        """
        Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive.
        """
        role = self.model.Role.get_by(name=role.lower())
        if role:
            return True
        return False
        
    def group_exists(self, group):
        """
        Returns ``True`` if the group exists, ``False`` otherwise. Groups 
        are case insensitive.
        """
        group = self.model.Group.get_by(name=group.lower())
        if group:
            return True
        return False
        
    # List Methods
    def list_roles(self):
        """
        Returns a lowercase list of all roll names ordered alphabetically
        """
        return [r.name for r in self.model.Role.select( \
           order_by=self.model.Role.c.name) ]
        
    def list_users(self):
        """
        Returns a lowecase list of all usernames ordered alphabetically
        """
        return [u.username for u in self.model.User.select( \
           order_by=self.model.User.c.username)]

    def list_groups(self):
        """
        Returns a lowercase list of all groups ordered alphabetically
        """
        return [g.name for g in self.model.Group.select( \
           order_by=self.model.Group.c.name)]

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
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        user = self.model.User.get_by(username=username.lower())
        roles = [r.name for r in user.roles]
        roles.sort()
        return {
            'username': user.username,
            'group':    user.group and user.group.name or None,
            'password': user.password,
            'roles':    roles
        }

    def user_roles(self, username):
        """
        Returns a list of all the role names for the given username ordered 
        alphabetically. Raises an exception if the username doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        roles = [r.name for r in self.model.User.get_by( \
           username=username.lower()).roles]
        roles.sort()
        return roles
        
    def user_group(self, username):
        """
        Returns the group associated with the user or ``None`` if no group is
        associated. Raises an exception is the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        return self.model.User.get_by(username=username.lower()).group.name
        
    def user_password(self, username):
        """
        Returns the password associated with the user or ``None`` if no
        password exists. Raises an exception is the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        return self.model.User.get_by(username=username.lower()).password

    def user_has_role(self, username, role):
        """
        Returns ``True`` if the user has the role specified, ``False`` 
        otherwise. Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.role_exists(role.lower()):
            raise AuthKitNoSuchRoleError("No such role %r"%role.lower())
        for role_ in self.model.User.get_by(username=username.lower()).roles:
            if role_.name == role.lower():
                return True
        return False
        
    def user_has_group(self, username, group):
        """
        Returns ``True`` if the user has the group specified, ``False`` 
        otherwise. The value for ``group`` can be ``None`` to test that 
        the user doesn't belong to a group. Raises an exception if the 
        user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if group is not None and not self.group_exists(group.lower()):
            raise AuthKitNoSuchGroupError("No such group %r"%group.lower())
        user = self.model.User.get_by(username=username.lower())
        if user.group is None:
            if group == None:
                return True
        else:
            if group is not None and user.group.name == group.lower():
                return True
        return False

    def user_has_password(self, username, password):
        """
        Returns ``True`` if the user has the password specified, ``False`` 
        otherwise. Passwords are case sensitive. Raises an exception if the
        user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        user = self.model.User.get_by(username=username.lower())
        if user.password == self.encrypt(password):
            return True
        return False
        
    def user_set_username(self, username, new_username):
        """
        Sets the user's username to the lowercase of new_username. 
        Raises an exception if the user doesn't exist or if there is already
        a user with the username specified by ``new_username``.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if self.user_exists(new_username.lower()):
            raise AuthKitError(
                "A user with the username %r already exists"%username.lower()
            )
        user = self.model.User.get_by(username=username.lower())
        user.username = new_username.lower()
        user.flush()
        
    def user_set_group(self, username, group, auto_add_group=False):
        """
        Sets the user's group to the lowercase of ``group`` or ``None``. If
        the group doesn't exist and ``add_if_necessary`` is ``True`` the 
        group will also be added. Otherwise an ``AuthKitNoSuchGroupError`` 
        will be raised. Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.group_exists(group.lower()):
            if auto_add_group:
                self.group_create(group.lower())
            else:
                raise AuthKitNoSuchGroupError("No such group %r"%group.lower())
        user = self.model.User.get_by(username=username.lower())
        user.group = self.model.Group.get_by(name=group.lower())
        user.flush()
        
    def user_add_role(self, username, role, auto_add_role=False):
        """
        Sets the user's role to the lowercase of ``role``. If the role doesn't
        exist and ``add_if_necessary`` is ``True`` the role will also be
        added. Otherwise an ``AuthKitNoSuchRoleError`` will be raised. Raises
        an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.role_exists(role.lower()):
            if auto_add_role:
                self.role_create(role.lower())
            else:
                raise AuthKitNoSuchRoleError("No such role %r"%role.lower())
        user = self.model.User.get_by(username=username.lower())
        role = self.model.Role.get_by(name=role.lower())
        user.roles.append(role)
        user.flush()
    
    def user_remove_group(self, username):
        """
        Sets the group to ``None`` for the user specified by ``username``.
        Raises an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        user = self.model.User.get_by(username=username.lower())
        user.group = None
        user.flush()
    
    def user_remove_role(self, username, role):
        """
        Removes the role from the user specified by ``username``. Raises 
        an exception if the user doesn't exist.
        """
        if not self.user_exists(username.lower()):
            raise AuthKitNoSuchUserError("No such user %r"%username.lower())
        if not self.role_exists(role.lower()):
            raise AuthKitNoSuchRoleError("No such role %r"%role.lower())
        user = self.model.User.get_by(username=username.lower())
        for role_ in user.roles:
            if role_.name == role.lower():
                user.roles.pop(user.roles.index(role_))
                user.flush()
                return
        raise AuthKitError(
            "No role %r found for user %r"%(role.lower(), username.lower())
        )

