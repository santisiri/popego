# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from zope.interface import Interface

class ICachePersistence(Interface):
    def invalidate(resource, newValue):
        """ TODO manu"""

    def getLastValue(resources):
        """ TODO """

#     def getDefaultTag():
#         """ TODO """

#     def clear():
#         """ TODO """

class IHitResponseGenerator(Interface):
    def responseFor(call):
        """ TODO """
    
class IActionMethodResolver(Interface):
    def get(*args, **kwargs):
        """ TODO """ 

class ITagManager(Interface):
    """ 
    Responsable de todo lo concerniente 
    a tags de cache. Esto implica generarlos,
    como asi también encontrarlos o ponerlos
    en la capa de transporte.

    Esta capa esta modelada como call (request
    entrantes) y retValues (responses)
    """
    
    def extractTag(call):
        """ Extrae el tag de cache de un call """
    def injectTag(tag, retValue):
        """ TODO """
    def newTag():
        """ TODO """
    def defaultTag():
        """ TODO """

# generador de 304
# generador 
