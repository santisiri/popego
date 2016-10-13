# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

class CacheConfig(object):
    """
    Configurador del Cache.
    En el se definen los recursos/esferas, y sobre que acciones
    cachean o invalidan.

    Si tuvieramos una clase cualquiera:
    >>> class SomeClass(object):
    ...     def aMethod(self, username=None):
    ...             pass
    ...     def aMethod2(self, bla=None):
    ...             pass
    ...

    y quisieramos definir un cache con dos tipos de recursos: Agents y User

    >>> config = CacheConfig()
    >>> s = config.defineResourceType('User')
    >>> s2 = config.defineResourceType('Agents')

    y reglas:

    >>> from popserver.lib.cache.fetchers import idOnParameter
    >>> s.invalidateOn(CodePoint(SomeClass.aMethod), idOnParameter('username'))
    >>> s.invalidateOn(CodePoint(SomeClass.aMethod2), idOnParameter('bla'))
    >>> s.cacheOn(CodePoint(SomeClass.aMethod), idOnParameter('username'))
    >>> s2.cacheOn(CodePoint(SomeClass.aMethod), idOnParameter('username'))

    nos daría:
    >>> config.iCacheActions()
    [(<CodePoint: <unbound method SomeClass.aMethod> >, [<ResourceFetcher type=User>, <ResourceFetcher type=Agents>])]
    >>> config.iInvalidateActions()
    [(<CodePoint: <unbound method SomeClass.aMethod> >, [<ResourceFetcher type=User>]), (<CodePoint: <unbound method SomeClass.aMethod2> >, [<ResourceFetcher type=User>])]
    """

    def __init__(self):
        self.cacheActions = dict()
        self.invalidateActions = dict()

    def defineResourceType(self, typeName):
        """ Define un nuevo tipo de Esfera y la retorna """
        return ResourceType(typeName, self)

    def _newInvalidateAction(self, codePoint, resourceFetcher):
        self.invalidateActions.setdefault(codePoint, [])
        self.invalidateActions[codePoint].append(resourceFetcher)

    def _newCacheAction(self, codePoint, resourceFetcher):
        self.cacheActions.setdefault(codePoint, [])
        self.cacheActions[codePoint].append(resourceFetcher)

    def iCacheActions(self):
        return self.cacheActions.items()

    def iInvalidateActions(self):
        return self.invalidateActions.items()

class ResourceType(object):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def invalidateOn(self, codePoint, idFetcher):
        """
        Define una regla de invalidación, basada en un determinado 
        ``actionPath`` (path a un controller method) y un ``idFetcher``
        (función que dado un ``Call`` retorna en resourceId)
        """
        self.config._newInvalidateAction(codePoint,
                                         ResourceFetcher(self.name, 
                                                         idFetcher))

    def cacheOn(self, codePoint, idFetcher):
        """
        Define una regla de cache, basada en un determinado 
        ``actionPath`` (path a un controller method) y un ``idFetcher``
        (función que dado un ``Call`` retorna en resourceId)
        """
        self.config._newCacheAction(codePoint,
                                   ResourceFetcher(self.name, idFetcher))


class ResourceFetcher(object):
    def __init__(self, type, idFetcher):
        self.type = type
        self.idFetcher = idFetcher

    def fetch(self, call):
        return (self.type, self.idFetcher(call))

    def __repr__(self):
        return "<ResourceFetcher type=%s>" % self.type


class CodePoint(object):
    def __init__(self, callable, condition=lambda x:True):
        self.callable = callable
        self.condition = condition

    def __eq__(self, other):
        if isinstance(other, CodePoint):
            return self.callable == other.callable \
                and self.condition == other.condition
        return False

    def __repr__(self):
        return "<CodePoint: %(callable)s >" % self.__dict__

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.callable) ^ hash(self.condition)
