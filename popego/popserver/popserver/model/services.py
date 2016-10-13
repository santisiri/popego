# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elixir import *
from sqlalchemy.types import *
from sqlalchemy import UniqueConstraint

# Model Path
MP = 'popserver.model.'

__all__ = ['ServiceType', 'Service', 'Account']

class ServiceType(Entity):
    """ Descriptor de tipo de servicio. Cada tipo sugiere un media distinto """
    id = Field(Integer, primary_key=True)
    type = Field(Unicode(64), nullable=False, unique=True)
    description = Field(Unicode(255))
    is_media = Field(Boolean(), nullable=False, default=True)
    services = OneToMany('Service')
    using_options(tablename='service_types')
    
    def __repr__(self):
        return "ServiceType(%(type)s)" % self.__dict__

    def getServicesForUser(self, user):
        """ 
        Retorna instancias de ``Service`` de este ``ServiceType`` para los 
        que ``user`` tiene un ``Account`` 
        """
        return Service.query.filter(Service.accounts.any(user_id=user.id)) \
            .filter_by(type_id=self.id).all()
   
class Service(Entity):
    """ 
    Descriptor de servicio.

    Es responsable de entregar un par (Agente, UserItemFactory) para realizar
    el fetch de la información de un usuario del servicio a popego
    """
    id = Field(Integer, primary_key=True)
    name = Field(Unicode(128), nullable=False, unique=True)
    description = Field(Unicode(256))
    url = Field(Unicode(255), nullable=False)
    prompt_text = Field(Unicode(256))
    added_text = Field(Unicode(256))
    agent = Field(Unicode(255)) # fully qualified name de la clase que implementa el agente. eg. 'popserver.agents.flickr_agent:FlickrAgent'
    item_factory = Field(Unicode(255)) # fully qualified name
    type = ManyToOne('ServiceType', colname='type_id', required=True, 
                     ondelete='restrict')
    accounts = OneToMany('Account')
    weight = Field(Float, nullable=False, default=1)

    using_options(tablename='services')
    
    def __repr__(self):
        return "Service(%(name)s)" % self.__dict__

    def getAgent(self):
        """
        Obtiene una instancia del agente correspondiente 
        para este ``Service``
        """
        return self._parseCodePath(self.agent)

    def getUserItemFactory(self, user):
        """ Retorna el UserItemFactory propio del Servicio """
        if self.item_factory is not None:
          clazz = self._parseCodePath(self.item_factory)
          return clazz(user, self)
        else:
          return None


    def userExists(self, username):
        """ 
        Chequea si ``username`` es un nombre de usuario válido para 
        este ``Service`` 
        """
        return self.getAgent().userExists(username)

    def _parseCodePath(self, path):
        if ':' in path:
            modulePath,attrs = path.split(':',1)

            needsCall = False
            if attrs.endswith('()'):
                attrs = attrs[:-2]
                needsCall = True
            attrs = attrs.split(".")
            obj = __import__(modulePath, fromlist=['__name__'])
            
            for attr in attrs:
                obj = getattr(obj, attr)
            if needsCall: 
                obj = obj()
        else:
            obj = __import__(path, fromlist=['__name__'])
        
        return obj


    def faviconURL(self):
        """ Retorna un URL al icono representativo de este Service """
        import re, string
        return '/images/icons/%s_favicon.png' % re.sub(r'\s', '_', self.name).lower()

       

class Account(Entity):
    """ Cuenta de usuario de un ``User`` en un ``Service`` """
    id = Field(Integer, primary_key=True)
    username = Field(Unicode(64), nullable=False)
    home_url = Field(Unicode(1024))
    last_updated = Field(DateTime)
    user = ManyToOne(MP + 'users.User', colname="user_id", required=True, 
                     ondelete='cascade',cascade='none')
    service = ManyToOne('Service', colname='service_id', required=True,
                        ondelete='restrict')
    item_groups = OneToMany(MP + 'items.ItemGroup', cascade='all,delete-orphan')
    using_options(tablename='accounts')

    using_table_options(UniqueConstraint('user_id','service_id'))
    
    def __repr__(self):
        if self.service:
            return "Account(username: %s - service: %s)" \
                % (self.username, self.service.name)
        else:
            return "Account(username: %s - service: %s)" \
                % (self.username, "None")
            
    
    def getItemGroup(self, external_id):
        result = filter(lambda g: g.external_id == external_id,
                        self.item_groups)
        
        return result[0] if len(result) == 1 else None
