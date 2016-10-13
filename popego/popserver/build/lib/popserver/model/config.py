# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elixir import *
from sqlalchemy.types import *

import pickle

__all__ = ['Country', 'ProfileConfig', 'GlobalConfig']

class Country(Entity):
    """ Descriptor de un País """
    using_options(tablename='countries')
    id = Field(Unicode(2), primary_key=True)
    name = Field(Unicode(64))

class ProfileConfig(Entity):
    uItemTagWeight = Field(Float, nullable=False)
    itemTagWeight = Field(Float, nullable=False)
    consumerWeight = Field(Float, nullable=False)
    producerWeight = Field(Float, nullable=False)

    using_options(tablename='profileconfig')

class GlobalConfig(Entity):
    """ Variable de Configuración Global del Sistema """
    using_options(tablename='globalconfig')
    property = Field(String, primary_key=True)
    value = Field(String, nullable=False)

    def __repr__(self):
        return "<%(property)s:%(value)s>" % self.__dict__

    @classmethod
    def getAsInt(clazz, key):
        return int(GlobalConfig.get(key).value)

    @classmethod
    def getAsString(clazz, key):
        return GlobalConfig.get(key).value

    @classmethod
    def getAsPython(clazz, key):
        return pickle.loads(GlobalConfig.get(key).value)

    @classmethod
    def setAsPython(clazz, key, value):
        gc = GlobalConfig.getOrCreate(key)
        gc.value = pickle.dumps(value)
        gc.flush()

    @classmethod
    def setAsInt(clazz, key, value):
        gc = GlobalConfig.getOrCreate(key)
        gc.value = value
        gc.flush()

    @classmethod
    def setAsString(clazz, key, value):
        gc = GlobalConfig.getOrCreate(key)
        gc.value = value
        gc.flush()

    @classmethod
    def getOrCreate(clazz, key):
        gc = GlobalConfig.get(key)
        if gc is None:
            gc = GlobalConfig(property=key)
        return gc
