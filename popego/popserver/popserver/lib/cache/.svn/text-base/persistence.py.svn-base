import api
from zope.interface import implements
from datetime import datetime

class MemoryCachePersistence(object):
    implements(api.ICachePersistence)

    def __init__(self):
        self.cache = dict()

    def invalidate(self, resource, newTag):
        self.cache[resource] = newTag


    def getLastValue(self, resources):
        if resources is None or len(resources) == 0:
            raise Exception, "Error en los parametros"

        lastRow = None
        for r in resources:
            row = self.cache.get(r, None)
            if row is not None and (lastRow is None or lastRow[1] < row[1]):
                lastRow = row
        return lastRow 

