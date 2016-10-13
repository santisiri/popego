# -*- coding: utf-8 -*-

"""
Decorator del modulo popserver.model.
Decora todas las clases del modulo para que al momento de la creación
se realize un expunge() y no esten acopladas a la base.

Esto se puede usar en los tests que no requieran ni quieran saber nada
de Bases de Datos y antes no podían porque elixir acoplaba cada instancia
con la DB.
"""

__docformat__='restructuredtext'


def __init__():
    wraps = __import__('functools', fromlist='__name__').wraps

    def decorator(clazz):
        @wraps(clazz)
        def cons(*args, **kwargs):
            instance = clazz(*args, **kwargs)
            instance.expunge()
            return instance
        return cons

    _model = __import__('popserver.model',fromlist='__name__')
    EntityMeta = __import__('elixir.entity',fromlist='__name__').EntityMeta
    modelClasses = [(name, o) for name,o in _model.__dict__.items() 
                    if type(o) is EntityMeta]

    me = __import__(__name__, fromlist='__name__')
    for name, clazz in modelClasses:
        setattr(me, name, decorator(clazz))
    

__init__()
del __init__
