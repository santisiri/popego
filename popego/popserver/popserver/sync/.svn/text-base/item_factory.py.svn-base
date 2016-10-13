# -*- coding: utf-8 -*-
""" 
Modulo con todos los UserItemFactories.

Cada UserItemFactory tiene su par en un Agent. Donde el Agente se encarga
de parsear el contenido de un Servicio y el UserItemFactory se encarga de
transformar el contenido parseado a ``UserItem``s, ``Item``s y ``Tag``s

"""
__docformat__='restructuredtext'

from datetime import datetime
from itertools import imap
from popserver.model import *
import exceptions
import logging

class AbstractUserItemFactory(object):
    """ 
    ``UserItem`` Factory, responsable de la creación de ``UserItem``s
    con sus respectivo ``Item`` y ``Tag``s.

    Su interfaz pública presenta un solo método:

     * create(self, itemExtId, attrs)

    Clase abstracta en forma de template method, para definir un nuevo
    UserItemFactory es necesario implementar los métodos:
    
     * newItem(self, attrs)
     * populateCustomItem(self, item, attrs)

    """
    def __init__(self, user, service):
        self.user = user
        self.service = service
        self.newItems = dict()
        self.newTags = dict()

    def create(self, itemExtId, attrs):
        """ 
        Crea y retorna un ``UserItem`` usando el external_id ``itemExtId`` y 
        un diccionario de attributos ``attrs``.

        Los atributos posibles son:
         
        Para el ``UserItem``
         * creation_date: ``datetime`` de creación en el Servicio
         * user_tags: [str] con los tags

        Para el ``Item``:
         * item_tags: [str] con los tags
         * title: str con el título del ``Item``
         * description: str con el título del ``UserItem``

        El resto de los atributos sera ignorado o tomado en cuenta por
        la subclase particular del template method.
        """
        item = self.getItem(itemExtId)
        if item is None:
            item = self.createItem(itemExtId,attrs)
        return self.createUserItem(item, attrs)

    def createItem(self, extId, attrs):
        """ Crea un ``Item``, asume que no existe ninguno con tal external_id"""
        item = self.newItem(attrs)
        item.external_id = extId
        self.populateItemAttrs(item,attrs)
        self.newItems[extId] = item
        return item

    def getItem(self, extId):
        """ 
        Retorna el ``Item`` con external_id == ``extId`` en caso de existir
        este en el cache de Items.

        El cache esta compuesto por la BD de Items, y los Items que todavía no
        han sido flusheados en ella, pero si parseados.
        """
        if extId in self.newItems:
            item = self.newItems[extId]
        else:
            item = Item.get_by(external_id=extId)
        return item

    def newItem(self,attrs):
        """ 
        Instancia (sin popular) un ``Item`` 
        
        A ser implementado por subclase
        """
        raise NotImplementedError("Abstract method")

    def createUserItem(self, item, attrs):
        """
        Crea un ``UserItem`` dado un ``Item`` ``item`` y
        un diccionario de atributos.

        Ver ``create()``
        """
        ui = UserItem()
        ui.creation_date = attrs.get('creation_date',None)
        ui.tags = self.names2Tags(attrs.get('user_tags',[]))
        ui.item = item
        ui.user = self.user
        return ui

    def populateItemAttrs(self, item, attrs):
        """
        Popula los atributos a un ``Item`` item.
        No debería ser overrideado, sino que se debe implementar
        ``populateCustomItem(self, item, attrs)``
        """
        item.service = self.service
        item.title = attrs.get('title',None)
        item.tags = self.names2Tags(attrs.get('item_tags',[]))
        item.description = attrs.get('description',None)
        self.populateCustomItem(item, attrs)

    def populateCustomItem(self,item, attrs):
        """
        Popula los atributos especiales del ``Item`` ``item`` con 
        el diccionario de atributos ``attrs``.
        
        A ser implementado por subclase
        """
        raise NotImplementedError("Abstract method")

    def names2Tags(self, names):
        """ 
        tipo: [str] -> [Tag]
        Recibe un [str] de strings no únicos, y lo transforma en [Tag] de
        tags únicos.
        """
        def name2Tag(name):
            if name in self.newTags:
                tag = self.newTags[name]
            else:
                tag = Tag.get_by(name=name)
                if tag is None: 
                    tag = Tag(name=name)
                    self.newTags[name] = tag
            return tag

        def toUnicode(name):
            # retorna un Unicode string para ``name`` o ``None`` si no es posible
            n = None
            try:
                n = unicode.strip(unicode(name))
            except exceptions.UnicodeDecodeError:
                pass
            return n
        
        return map(name2Tag, set(filter(lambda i: i is not None, map(toUnicode, names))))
        
class YoutubeUserItemFactory(AbstractUserItemFactory):
    def newItem(self, attrs):
        return Video()

    def populateCustomItem(self, item, attrs):
        item.externalURL = attrs['externalURL']
        item.embedURL = attrs['embedURL']
        item.author =  attrs['author']
        item.thumbnails = map(self.map2thumbnail, attrs['thumbnails'])

    def map2thumbnail(self, th):
        return VideoThumbnail(width=th['width'], height=th['height'],
                              url=th['url'], time=th['time'])

class DeliciousUserItemFactory(AbstractUserItemFactory):
    def newItem(self, attrs):
        return Bookmark()

    def populateCustomItem(self, item, attrs):
        item.url = attrs['url']
        item.popularity = attrs['popularity']
        item.serviceUrl =  attrs['serviceUrl']


class FlickrUserItemFactory(AbstractUserItemFactory):
    def newItem(self, attrs):
        return Photo()

    def populateCustomItem(self, item, attrs):
        item.url = attrs['url']
        item.thumbnail_url = attrs['thumbnail_url']
        item.external_url = attrs['external_url']

class LastFMUserItemFactory(AbstractUserItemFactory):

    def newItem(self, attrs):
        rv = None
        if 'photo_url' in attrs:
            rv = Artist()
        else:
            rv = Song()
        
        return rv

    def populateCustomItem(self, item, attrs):
        if isinstance(item, Artist):
            item.photo_url = attrs['photo_url']
        else:
            # linkear o crear el Artist asociado a item (Song)
            artistExtId = attrs['artist']['external_id']
            artist = self.getItem(artistExtId)
            if artist is None:
                artist = self.createItem(artistExtId,attrs['artist'])

            item.artist = artist

    def createUserItem(self, item, attrs):
        ui = None
        if isinstance(item, Song):
            ui = SongUserItem(play_count=attrs.get('playcount', None))
        elif isinstance(item, Artist):
            ui = ArtistUserItem(play_count=attrs['playcount'])
        
        ui.creation_date = attrs.get('creation_date', datetime.utcnow())
        ui.tags = self.names2Tags(attrs.get('user_tags',[]))
        ui.item = item
        ui.user = self.user
        return ui

class BlogUserItemFactory(AbstractUserItemFactory):
    def newItem(self, attrs):
        return Article()

    def populateCustomItem(self, item, attrs):
	item.external_url = attrs['external_url']
	item.publish_date = attrs['creation_date'] # for Item (not UserItem)

class TwitterUserItemFactory(AbstractUserItemFactory):
    def newItem(self, attrs):
        return Quote()

    def populateCustomItem(self, item, attrs):
	item.external_url = attrs['external_url']

