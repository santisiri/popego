# -*- coding: utf-8 -*-
__docformat__='restructuredtext'


from authkit.users import md5
from elixir import *
from elixir.events import after_insert
from sqlalchemy.types import *
from popserver.model import services

# Model Path
MP = 'popserver.model.'

__all__ = ['User', 'Group', 'Role', 'UserRole', 'Feedback', 'Widget']

secret = 'popego secret string'


class User(Entity):
    """ Un usuario del sistema. """

    id = Field(Integer, primary_key=True)
    displayname = Field(Unicode(255), unique=False, nullable=False)
    username = Field(Unicode(255), unique=True, nullable=False)
    _password = Field(Unicode(255), nullable=False, colname='password', 
                      synonym='password')
    photo = Field(Unicode(255)) # TODO: este campo se esta usando???
    email = Field(Unicode(50), unique=True, nullable=False)
    shortBio = Field(Unicode(255))
    website = Field(Unicode(64))
    gender = Field(Unicode(1))
    birthdate = Field(DateTime)
    avatar_mtime = Field(DateTime)
    country = ManyToOne(MP + 'config.Country', colname='country_id', 
                        ondelete='restrict')
    group = ManyToOne('Group', colname='group_id')
    accounts = OneToMany(MP + 'services.Account', cascade='all, delete-orphan', 
                         passive_deletes=True)
    tagCounts = OneToMany(MP + 'items.TagCount', cascade='all, delete-orphan', 
                          passive_deletes=True)
    weightedObjCount = Field(Float, nullable=False, default=0)
    widgets = OneToMany('Widget', cascade='all, delete-orphan', 
                          passive_deletes=True)
    using_options(tablename='users')

    # Se hashea la password con MD5
    def _set_password(self, password):
       self._password = md5(password, secret)
    def _get_password(self):
       return self._password
    password = property(_get_password, _set_password)

    def changePassword(self, currentpass, newpass, confirm):
	if newpass == confirm and self.password == md5(currentpass, secret):
		self._set_password(newpass)
		return True
	return False

    def __repr__(self):
        return "User(%(username)s)" % self.__dict__

    def getAccountsByType(self, type):
        """ Retorna las Accounts del usuario de un tipo de servicio dado"""
	return [i for i in self.accounts if i.service.type.type == type]
	# TODO: mejorar eficiencia de la consulta?

    @after_insert
    def _post_insert(self):
        """ Cada vez que se agrega un usuario se crea un widget default """
        # TODO Soportar varios widgets para el mismo user
        widget = Widget(id=1, user=self)
        self.widgets.append(widget)
        widget.flush()
        
          
# Entidades necesarias para AuthKit
class Group(Entity):
    """ Grupo de Usuarios, para reglas de seguridad """
    id = Field(Integer, primary_key=True)
    name = Field(Unicode(255), unique=True, nullable=False)
    using_options(tablename='groups')

    def __repr__(self):
        return "Group(%(name)s)" % self.__dict__

class Role(Entity):
    id = Field(Integer, primary_key=True)
    name = Field(Unicode(255), unique=True, nullable=False)
    using_options(tablename='roles')

class UserRole(Entity):
    user = ManyToOne('User', colname='user_id')
    role = ManyToOne('Role', colname='role_id')
    using_options(tablename='users_roles')

    
class Feedback(Entity):
    """ Mensaje de Feedback de un Usuario """
    id = Field(Integer, primary_key=True)
    type = Field(Unicode(32), nullable=False)
    comment = Field(Unicode(255), nullable=False)
    creation_date = Field(DateTime, nullable=False)
    user_agent = Field(Unicode('255'))
    user = ManyToOne('User', required=False, colname='user_id')
    using_options(tablename='feedback')
    

class Widget(Entity):
    id = Field(Integer, primary_key=True)
    template = Field(Unicode(50))
    theme = Field(Unicode(16))
    best_referrer = Field(Unicode(255))
    last_seen = Field(DateTime)
    user = ManyToOne('User', colname='user_id', primary_key=True, ondelete='cascade')
    using_options(tablename='widgets')

    def getTheme(self):
        return self.theme or 'ff3366'
