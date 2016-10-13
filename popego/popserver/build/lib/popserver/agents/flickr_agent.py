# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import logging

import flickr_client.FlickrClient as flickr
import popserver.model

from datetime import datetime
import string

log = logging.getLogger(__name__)

class FlickrAgent:

    PER_PAGE = 50

    def __init__(self):
        # init flickr library
        # host, api_endpoint, api_key: module level attrs (inicialización hecha por agents.__init__)
        flickr.HOST = host
        flickr.API  = api_endpoint
        self.flickrClient = flickr.FlickrClient(flickr.API_KEY)

    def userExists(self, cred):
        return self._getUserId(cred) is not None

    def updateAccount(self, account, cacheApi):
        self.account = account

        self.flickrUserID = self._getUserId(account.username)

        if account.home_url is None:
            account.home_url = "http://www.flickr.com/photos/%s" % self.flickrUserID

        # create null group
        if not cacheApi.groupExists(None):
            cacheApi.addGroup(None, name='Flickr(%s)' % account.username, is_null_group=True)

        doSync = True

        page = 1
        photos = self.getItems(page=page, per_page=FlickrAgent.PER_PAGE)

        while doSync and photos != []:
            for photo in photos:
                if (account.last_updated is not None) and (photo['creation_date'] < account.last_updated):
                    doSync = False
                    break

                photo_id = photo['external_id']
                del(photo['external_id'])
                cacheApi.addItem(photo_id, photo)
                
                groups = self.getItemGroups(photo_id)
                if len(groups) > 0:
                    for g in groups:
                        group_id = g['external_id']
                        del(g['external_id'])
                        if not cacheApi.groupExists(group_id): 
                            cacheApi.addGroup(group_id, **g)
                    cacheApi.bindItem2Group(group_id, photo_id)
                else:
                    cacheApi.bindItem2Group(None, photo_id)

            if not doSync: break
            page += 1
            photos = self.getItems(page=page, per_page=FlickrAgent.PER_PAGE)
            
    def getItems(self, page=1, per_page=100):
        flickr_items = self.flickrClient.flickr_people_getPublicPhotos(user_id=self.flickrUserID, per_page=per_page, page=page)[0]
        items = []
        for p in flickr_items:
            flickr_photo = self.flickrClient.flickr_photos_getInfo(photo_id=p('id'))
            i = self._buildItem(flickr_photo[0])
            items.append(i)
        return items

    def getItemGroups(self, photo_external_id):
        """ Obtiene los ItemGroup (Photoset) al que pertenece ésta foto """
        contexts = self.flickrClient.flickr_photos_getAllContexts(photo_id=photo_external_id)
        groups = []
        if contexts is not None and len(contexts) > 0:
            for set in filter(lambda g: g._name == 'set', contexts) or []:
                groups.append({ 'name' : set('title'),
                                'external_id' : str(set('id')),
                                'is_null_group' : False })

        return groups


    def _getItemVersionURL(self, farm_id, server_id, id, secret, version='m'):
        """ Generación de URLS documentada en http://www.flickr.com/services/api/misc.urls.html """
        return "http://farm%s.static.flickr.com/%s/%s_%s%s.jpg" % (farm_id, server_id, id, secret, '' if version == 'm' else '_' + version)

    def _buildItem(self, photo):
        photo = {
            'external_id' : photo('id'),
            'title' : unicode(photo.title),
            'description' : unicode(photo.description),
            'creation_date' : datetime.utcfromtimestamp(int(photo.dates('posted'))),
            'url' : self._getItemVersionURL(photo('farm'), 
                                            photo('server'), 
                                            photo('id'), 
                                            photo('secret')),
            'thumbnail_url' : self._getItemVersionURL(photo('farm'), 
                                                      photo('server'), 
                                                      photo('id'), 
                                                      photo('secret'), 
                                                      version='t'),
            'external_url' : "http://www.flickr.com/photos/%s/%s" % (self.flickrUserID, photo('id')),
            'item_tags' : map(lambda t: string.strip(str(t)), 
                         filter(lambda t: t('author') == self.flickrUserID and t('machine_tag') == '0', 
                                photo.tags))
            
            }
        return photo


    def _getUserId(self, cred):
        """ Retorna un NSID de usuario dado su username o su email """
        try:
            rv = self.flickrClient.flickr_people_findByEmail(find_email=cred) if '@' in cred \
                else self.flickrClient.flickr_people_findByUsername(username=cred)
        except flickr.FlickrError:
            return None
    
        return rv[0]('id')
        
