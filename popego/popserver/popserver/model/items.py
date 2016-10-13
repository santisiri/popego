# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elixir import *
from sqlalchemy.types import *
from sqlalchemy import UniqueConstraint
from datetime import datetime


# Model Path
MP = 'popserver.model.'

#__all__ = ['ItemGroup', 'OrderedUserItem', 'UserItem', 'SongUserItem', 'Item', 
__all__ = ['ItemGroup', 'OrderedUserItem', 'UserItem', 'SongUserItem', 'ArtistUserItem', 'Item', 
           'Photo', 'Video', 'Bookmark', 'VideoThumbnail', 'Artist', 'Song', 
           'Tag', 'TagCount', 'Article', 'Quote']

# TODO Chequeos de consistencia
#  * Todos los items tienen que ser del mismo tipo? servicio? Se viene un trigger o desde el modelo?
#  * Validar que el null group sea único para cada account
class ItemGroup(Entity):
    """ Grupo de ``UserItem``s. Relacionado a un ``Account`` """
    using_options(tablename='itemgroups')
    using_table_options(UniqueConstraint('external_id', 'account_id'))

    id = Field(Integer, primary_key=True)
    import_date = Field(DateTime)
    name = Field(Unicode(255), nullable=False)
    description = Field(Unicode(512))
    external_id = Field(Unicode(255), nullable=False)
    is_null_group = Field(Boolean, nullable=False, default=False)
    _orderedItems = OneToMany('OrderedUserItem', order_by='position',
                              cascade='all, delete-orphan', 
                              passive_deletes=True)
    account = ManyToOne(MP + 'services.Account', colname='account_id', 
                        ondelete='cascade', required=True)
    


    def __init__(self,*args,**kwargs):
        super(self.__class__, self).__init__(*args,**kwargs)
        self.import_date = datetime.utcnow()
    
    def __repr__(self):
        return "ItemGroup(external_id=%s)" % (self.external_id,)
    
    def _set_items(self, userItems):
        del self._orderedItems[:]
        
        orderedItems = []
        for i in range(len(userItems)):
            orderedItems.append(OrderedUserItem(userItem=userItems[i],
                                                position=i))
        self._orderedItems = orderedItems
       
    def _get_items(self):
        class OrderedToUserItemAdapter(object):
          def __init__(self, orderedItems):
                self.orderedItems = orderedItems

          def _toUserItem(self, orderedItem):
            return orderedItem.userItem
        
          def _toUserItemList(self):
            return [self._toUserItem(orderedItem) 
                    for orderedItem in self.orderedItems]
            
          def _toOrderedUserItem(self, userItem, position):
            return OrderedUserItem(userItem=userItem, position=position)
          
          def __len__(self):
            return self.orderedItems.__len__()
        
          def __getitem__(self, key):
            return self._toUserItem(self.orderedItems.__getitem__(key))
        
          def __setitem__(self, key, value):
            self.orderedItems[key].delete()  
            self.orderedItems.__setitem__(key, 
                        self._toOrderedUserItem(userItem=value, position=key))
        
          def __delitem__(self, key):
            self.orderedItems.__delitem__(key)
        
          def __iter__(self):
            return self._toUserItemList().__iter__()
        
          def __contains__(self, item):
            return self._toUserItemList().__contains__(item)
        
          def __getslice__(self, i, j):
            return self._toUserItemList().__getslice__(i,j)
        
          def __setslice__(self, i, j, sequence):
            raise NotImplementedError
        
          def __delslice__(self, i, j):
            return self.orderedItems.__delslice__(i,j)
        
          def __eq__(self, obj):
            return self._toUserItemList() == obj
        
          def __ne__(self, obj):
            return not self.__eq__(obj)
        
          def append(self, value):
            self.orderedItems.append(self._toOrderedUserItem(userItem=value,
                                               position=len(self.orderedItems)))

          def remove(self, value):
            for i, item in enumerate(self.orderedItems):
                if item.userItem is value:
                    del(self.orderedItems[i])
                    break
          
          def __repr__(self):
            return self._toUserItemList().__repr__()
        
        return OrderedToUserItemAdapter(self._orderedItems)

    items = property(_get_items, _set_items)



class OrderedUserItem(Entity):
    group = ManyToOne('ItemGroup', colname='itemgroups_id', 
                      ondelete='cascade', required=True, primary_key=True)
    userItem = ManyToOne('UserItem', colname='user_items_id', 
                         ondelete='restrict', required=True, 
                         primary_key=True)
    position = Field(Integer, nullable=False)
    
    using_options(tablename='itemgroups_items')
    
    def __repr__(self):
        return "OrderedUserItem(user_item_id=%(user_items_id)s, position=%(position)d)" % self.__dict__
    
class UserItem(Entity):
    """ 
    Representa la relación entre un ``Item`` y un ``User``.
    Existen atributos de relación que son aquellos que el usuario
    asigna al Item en el uso del Servicio dado
    """

    id = Field(Integer, primary_key=True)
    creation_date = Field(DateTime)
    import_date = Field(DateTime)
    item = ManyToOne('Item', colname='item_id', required=True, 
                     ondelete='restrict')
    _tags = ManyToMany('Tag', tablename='tags_useritems')
    user = ManyToOne(MP + 'users.User', colname="user_id", required=True, 
                     ondelete='cascade')
    
    using_options(tablename='user_items', inheritance='single', 
                  polymorphic=True)
    using_table_options(UniqueConstraint('user_id', 'item_id'))
    
    def __init__(self,*args,**kwargs):
        Entity.__init__(self, *args, **kwargs)
        # super(self.__class__, self).__init__(*args, **kwargs)
        self.import_date = datetime.utcnow()

    def __repr__(self):
        return "UserItem(id=%s, item_id=%s, item_title=%s)" % \
            (self.id, self.item_id, self.item and self.item.title or '')

    def _get_tags(self):
        if len(self._tags) > 0: return self._tags
        else: return self.item.tags
    def _set_tags(self, tag_values):
        self._tags = tag_values
    tags = property(_get_tags, _set_tags)
    
class UserItemWithPlaycount(UserItem):
    
    has_field('play_count', Integer)
    using_options(inheritance='single', polymorphic=True)

class SongUserItem(UserItemWithPlaycount):
    
    using_options(inheritance='single', polymorphic=True)

class ArtistUserItem(UserItemWithPlaycount):

    using_options(inheritance='single', polymorphic=True)


       
class Item(Entity):
    """
    Representa a un Item de un ``Service``.
    Cada subclase de Item representa a un tipo diferente de media.
    """
    id = Field(Integer, primary_key=True)
    import_date = Field(DateTime)
    service = ManyToOne(MP + 'services.Service', colname='service_id', ondelete='restrict', 
                        required=True)
    external_id = Field(Unicode(2048), nullable=False)
    title = Field(Unicode(255))
    _description = Field(Unicode(512))

    tags = ManyToMany('Tag', tablename='tags_items')
    
    using_table_options(UniqueConstraint('external_id', 'service_id'))
    using_options(tablename='items', inheritance='multi', polymorphic=True)
    
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.import_date = datetime.utcnow()

    # Se trunca la descripcion
    def _set_description(self, description):
       if description is not None and len(description) > 512:
           description = description[0:509] + '...'
       self._description = description    
    def _get_description(self):
       return self._description
    description = property(_get_description, _set_description)

    def addTags(self, tag_list):
        """ agrega los tags (strings) en ``tag_list`` a este ``Item`` """
        for t in tag_list:
            t = t.strip()
            tag = Tag.get_by(name=t)
            if tag is None: tag = Tag(name=t)
            self.tags.append(tag)                
            
    def __repr__(self):
        return "Item(title=%(title)s, external_id=%(external_id)s" \
            % self.__dict__
            
class Photo(Item):
    url = Field(Unicode(2048), nullable=False)
    thumbnail_url = Field(Unicode(2048))
    external_url = Field(Unicode(512))
    using_options(tablename='photos', inheritance='multi', polymorphic=True)
                
    def __repr__(self):
        return "Photo(service=%s, external_id=%s)" \
            % (self.service.name, self.external_id)
                
class Video(Item):
    thumbnails   = OneToMany('VideoThumbnail', cascade="all, delete-orphan", 
                             passive_deletes=True)
    externalURL  = Field(Unicode(2048), nullable=False)
    embedURL     = Field(Unicode(2048), nullable=False)
    author       = Field(Unicode(100))
    
    using_options(tablename='videos', inheritance='multi', polymorphic=True)
                    
    def __repr__(self):
        return "Video(title=%s)" % self.title

class VideoThumbnail(Entity):
    using_options(tablename='videothumbnails')
    url = Field(Unicode(255), nullable=False)
    height = Field(Integer)
    width  = Field(Integer)
    time   = Field(String(20))
    video  = ManyToOne('Video', required=True, ondelete='cascade')

class Bookmark(Item):
    using_options(tablename='bookmarks', inheritance='multi', polymorphic=True)

    url = Field(Unicode(2048), nullable=False)
    serviceUrl = Field(Unicode(2048), nullable=False)
    popularity = Field(Integer, nullable=False)

    def __repr__(self):
      return "Bookmark(service=%s, external_id=%s)" \
          % (self.service.name, self.external_id)

class Artist(Item):
    using_options(tablename='artists', inheritance='multi', polymorphic=True)

    photo_url = Field(Unicode(512))
    songs = OneToMany('Song')
    

class Song(Item):
    using_options(tablename='songs', inheritance='multi', polymorphic=True)

    artist = ManyToOne('Artist', required=True, ondelete='restrict')
    

class Tag(Entity):
    id = Field(Integer, primary_key=True)
    name = Field(Unicode(256), nullable=False)
    user_items = ManyToMany('UserItem', tablename='tags_useritems')
    items = ManyToMany('Item', tablename='tags_items')
    tag_counts = OneToMany('TagCount', cascade='all, delete-orphan', 
                           passive_deletes=True) # TODO fijarse si está bien

    using_options(tablename='tags')
    using_table_options(UniqueConstraint('name'))

    def __repr__(self):
        return "Tag(name=%s)" % self.name
    
class TagCount(Entity):
    """ Reprenta la cantidad de hits de un determinado ``Tag`` en un ``User``"""
    user = ManyToOne(MP + 'users.User', colname='user_id', ondelete='cascade',
                     required=True, primary_key=True)
    count = Field(Integer, nullable=False)
    # TODO eagerload?
    tag = ManyToOne('Tag', colname='tag_id', ondelete='restrict',
                    required=True, primary_key=True)
    weightedCount = Field(Float, nullable=False)
    interest_factor = Field(Integer, nullable=False, default=0)

    using_options(tablename='tagcounts')

    def __repr__(self):
        return "TagCount(user=%s, tag=%s, count=%d, ifactor=%d)" \
            % (self.user, self.tag, self.count, self.interest_factor)

class Article(Item):
    publish_date = Field(DateTime, nullable=False) # (or update date if n/a)
    external_url = Field(Unicode(2048), nullable=False)
    # TODO: para entries de feed readers se podria incluir:
    #author = Field(Unicode(100))
    #source_title = Field(Unicode(100)) # fuente de info (e.g.: Slashdot)
    #source_url = Field(Unicode(100)) # (e.g.: http://slashdot.org)
    
    using_options(tablename='articles', inheritance='multi', polymorphic=True)
                    
    def __repr__(self):
        return "Article(title=%s)" % self.title

class Quote(Item):
    external_url = Field(Unicode(1024), nullable=False)
    
    using_options(tablename='quotes', inheritance='multi', polymorphic=True)
                    
    def __repr__(self):
        return "Quote(title=%s)" % self.title


