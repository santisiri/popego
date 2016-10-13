# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from formencode import Schema
from formencode.validators import *
from sqlalchemy.sql import select, func
import elixir

class Unique(FancyValidator):

    def __init__(self,entity,attribute,**kwargs):
        #self.super = super(self.__class__,self)
        #self.super.__init__(**kwargs)
	# TODO: ver como es la mejor forma de invocar al constructor padre
	# ante casos de herencia de mas de un nivel
        FancyValidator.__init__(self, **kwargs)
        self.entity = entity
        self.attribute = attribute
    
    def _to_python(self,value,state):
        return value

    def _from_python(self, value, state):
        return value

    def validate_python(self, value, state):
        count = self.entity.query.filter_by(**{self.attribute:value}).count()
        if count > 0:
            raise Invalid('%s already exists' % self.attribute, value, state)

class UniqueCaseInsensitive(Unique):
    def __init__(self,entity,attribute,**kwargs):
        Unique.__init__(self, entity, attribute, **kwargs)
    
    def validate_python(self, value, state):
	conn = elixir.metadata.bind.connect()
	s = select([func.count(getattr(self.entity, self.attribute))]) \
		.where(func.lower(getattr(self.entity, self.attribute)) \
		.like(func.lower(value)))
	count = conn.execute(s).fetchall()[0][0]
        if count > 0:
            raise Invalid('%s already exists' % self.attribute, value, state)

class Chain(FancyValidator):
    def __init__(self, *validators):
        self.validators = validators
    def to_python(self,value, state=None):
        return reduce(lambda v,fn: fn.to_python(v,state),
                      self.validators, value)

    def _from_python(self,value,state):
        return reduce(lambda v,fn: fn._from_python(v,state),
                      self.validators.reverse(),value)

    def validate_python(self, value, state):
        for validator in self.validators:
            validator.validate_python(value, state)

    def validate_other(self, value, state):
        for validator in self.validators:
            validator.validate_other(value, state)
