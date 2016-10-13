# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elixir import *
from sqlalchemy.types import *
from sqlalchemy import UniqueConstraint

# Model Path
MP = 'popserver.model.'

__all__ = ['CacheResource']


class CacheResource(Entity):
    """ Identifica a un Recurso Cacheable """
    type = Field(Unicode(100), primary_key=True)
    id = Field(Unicode(100), primary_key=True)
    tag = Field(Unicode(100))
    last_modified = Field(DateTime)
    using_options(tablename='cache_resource')
    
    def __repr__(self):
        return "<Resource '%(type)s - %(id)s' tag:%(tag)s>" % self.__dict__
