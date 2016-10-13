from __future__ import absolute_import
import functools

__all__ = ['memo','retry']

def retry(maxRetries, *exceptions):
    """
    Retry Decorator. Realizar un retry de la funcion
    si esta levanta alguna de las ``exceptions``. Hace
    tantos retries como ``maxRetries``.
    """
    def _doDecoration(fn):
        def _doRetry(*args, **kwargs):
            retries = 0
            while retries <= maxRetries:
                try:
                    return fn(*args, **kwargs)
                except tuple(exceptions):
                    retries +=1
                    if retries > maxRetries:
                        raise
                    
        return _doRetry
    return _doDecoration

def memo(qty):
    """ 
    Decorator para funciones con transparencia referncial.
    Implementa un cache de ``qty`` llamadas para evitar
    calculos repetidos.
    """
    def decorator(f):
        decoratee = Memo(qty,f)
        return functools.wraps(f)(decoratee)
    return decorator

def compose(f,g):
    """ Compone dos funciones """
    def composed(*args,**kwargs):
        return f(g(*args, **kwargs))
    return composed

class Memo(object):
    def __init__(self, qty, fn):
        self.cache = FixedSizeCache(qty)
        self.fn = fn

    def __call__(self,*args,**kwargs):
        key = (args,kwargs)
        if key in self.cache:
            retValue = self.cache[key]
        else:
            retValue = self.fn(*args,**kwargs)
            self.cache[key] = retValue
        return retValue

    def clear(self):
        self.cache.clear()
    def showCache(self):
        return self.cache


class FixedSizeCache(object):
    def __init__(self, size):
        self.size = size
        self.values = []
    def __getitem__(self,key):
        for k,v in self.values:
            if k == key:
                return v
        return None
    def __setitem__(self,key,value):
        self.values.append((key,value))
        if len(self.values) > self.size:
            self.values.pop(0)
    def __contains__(self,key):
        for k,v in self.values:
            if k == key:
                return True
        return False
    def __delitem__(self,key):
        raise NotImplementedError("Unsupported Operation")

    def __iter__(self):
        return self.values.__iter__()

    def keys(self):
        return [k for k,v in self.values]

    def clear(self):
       self.values = []


def mapDict(f, a):
    newDict = {}
    for k in a.keys():
        newDict[k] = f(a[k])
    return newDict

def izipDictWith(f, keys, a, b):
    for k in keys:
        yield f(k, a[k], b[k])

def findFirst(predicate, iterable):
    for i in iterable:
        if predicate(i):
            return i
    return None

def all(predicate, iterable):
    for i in iterable:
        if not predicate(i):
            return False
    return True
