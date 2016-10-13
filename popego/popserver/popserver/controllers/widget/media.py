# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import logging
import math

from popserver.lib.base import *
from popserver.lib.util import interval_of_time_in_words
from popserver.model import *
from datetime import datetime

log = logging.getLogger(__name__)

class MediaController(BaseController):

    def _getConfigVar(self,name):
        """
        Get Int configuration variables.
        Valid names:
         * groupsPageSize
         * picturesPageSize
         * videosPageSize
         * bookmarksPageSize
         * ranksPageSize
        """
        return GlobalConfig.getAsInt('popcard.media.' + name)

    def _groups(self, typeName, username, page):
        c.user = User.get_by(username=username)
        groupsQuery = ItemGroup.query\
            .join(['account','service','type']) \
            .filter(ServiceType.type == typeName ) \
            .filter(Account.user_id  == c.user.id)
        
        pageSize = self._getConfigVar('groupsPageSize')

        c.pageCount = math.ceil(groupsQuery.count() / float(pageSize))
        page = int(page)
        if page > c.pageCount or page <= 0: abort(500,'Invalid Page Number')
        
        offset = (page - 1) * pageSize
        c.groups = groupsQuery[offset:offset + pageSize].all()
        return render('/widget/media/%s/groups.mako' % typeName)



    def picturesGroups(self, username, page):
        return self._groups('pictures', username, page)

    ## TODO: picturesXXXX y videosXXXX son practicamente lo mismo -> refactorear
    def videosGroups(self, username, page):
        return self._groups('videos', username, page)

    def _thumbs(self, typeName, username, groupId, page):
        c.user = User.get_by(username=username)
        page = int(page)
        #TODO: migrate para cambiar el pageSize
        #pageSize = self._getConfigVar('%sPageSize' % typeName)
        pageSize = 55
        
        if groupId == "0":
            if typeName == "pictures":
                type = 'photo'
            else:
                type = 'video'
                
            items = UserItem.query.filter(UserItem.user_id == c.user.id)\
            .join('item').filter(Item.row_type == type) \
            .order_by(UserItem.creation_date.desc()).all();
            
            offset = 0
            pageSize *= page
            c.group = None
            
            c.albums = ItemGroup.query.join(['account', 'service', 'type'])\
            .filter(Account.user == c.user).filter(ServiceType.type == typeName).all()
        else:
            c.group = ItemGroup.query.get(groupId)
            items = c.group.items
            
            if page > c.pageCount or page <= 0: abort(500,'Invalid Page Number')
            offset = (page - 1) * pageSize
            
        c.pageCount = int(math.ceil(len(items) / float(pageSize)))
        c.items = items[offset:offset + pageSize]
        
        if page > 1 and typeName == "pictures":
            return render('/widget/media/%s/thumbs-content.mako' % typeName)
        else:
            return render('/widget/media/%s/thumbs.mako' % typeName)

    def picturesThumbs(self, username, groupId, page):
        return self._thumbs('pictures', username, groupId, page)

    def videosThumbs(self, username, groupId, page):
        return self._thumbs('videos', username, groupId, page)


    def _showcase(self, typeName, username, groupId, itemId):
        c.account = ItemGroup.query.get(groupId).account
        c.userItem = UserItem.query.get(itemId)
        return render('/widget/media/%s/showcase.mako' % typeName)        
    
    def picturesShowcase(self, username, groupId, itemId):
        return self._showcase('pictures', username,groupId, itemId)

    def videosShowcase(self, username, groupId, itemId):
        return self._showcase('videos', username,groupId, itemId)


    def bookmarks(self, username, page):
        c.user = User.get_by(username=username)
        page = int(page)

    	query =  UserItem.query.filter(UserItem.user_id == c.user.id)\
            .join('item').filter(Item.row_type == 'bookmark') \
            .order_by(UserItem.creation_date.desc())

        totalBkms = query.count()
        pageSize = self._getConfigVar('bookmarksPageSize')
        c.pageCount = int(math.ceil(totalBkms / float(pageSize)))
        c.page = page
        if page > c.pageCount or page <= 0: abort(500,'Invalid Page Number')

        offset = (page - 1) * pageSize
        c.userItems = query[offset:offset + pageSize].all()

        return render('/widget/media/bookmarks/index.mako')
    
    def music(self, username, page):
        c.user = User.get_by(username=username)


        recentSongs = ItemGroup.query\
            .filter(ItemGroup.name == 'Recently Listened')\
            .join('account').filter(Account.user_id == c.user.id).one()

        if len(recentSongs.items) >0:
            c.lastSong = recentSongs.items[0]
        else:
            c.lastSong = None

        ##Estoy pasando todos los artistas favoritos aunque no los necesito
        topArtistsGroup = ItemGroup.query\
            .filter(ItemGroup.external_id == 'top_artists')\
            .join('account').filter(Account.user_id == c.user.id).one()
        c.favoriteArtists = [x.item for x in topArtistsGroup.items[:2]]
        c.favoriteArtistsDate = topArtistsGroup.account.last_updated
        
        ##TODO: Cantidad de veces escuchada
        topTracksGroup = ItemGroup.query\
            .filter(ItemGroup.external_id == 'top_tracks')\
            .join('account').filter(Account.user_id == c.user.id).one()

        if len(topTracksGroup.items) > 0:
            c.favoriteSong = topTracksGroup.items[0].item
            c.favoriteSongPlays = topTracksGroup.items[0].play_count
            c.favoriteSongDate = topTracksGroup.account.last_updated
        else:
            c.favoriteSong = None
            c.favoriteSongPlays = None
            c.favoriteSongDate = None
        
        #Default images
        c.defaultArtistImage = GlobalConfig.getAsString('popcard.default.images.artist')
        
        return render('/widget/media/music/index.mako')
    
    def musicRanks(self, username, rank, page):
        c.user = User.get_by(username=username)
        c.rank = rank
        
        page = int(page)
        if page > c.pageCount or page <= 0: abort(500,'Invalid Page Number')
        offset = (page - 1) * self._getConfigVar('ranksPageSize')
        
        if (rank == 'LastTracks'):
            group = ItemGroup.query\
                .filter(ItemGroup.name == 'Recently Listened')\
                .join('account').filter(Account.user_id == c.user.id).one()
        elif (rank == 'TopArtists'):
            group = ItemGroup.query\
                .filter(ItemGroup.name == 'Top Artists')\
                .join('account').filter(Account.user_id == c.user.id).one()
        elif (rank == 'TopSongs'):
            group = ItemGroup.query\
                .filter(ItemGroup.name == 'Top Tracks')\
                .join('account').filter(Account.user_id == c.user.id).one()
        else:
            abort(404, "Invalid Rank")
        
        ##items = [x.item for x in group.items]
        items = group.items
        c.pageSize = self._getConfigVar('ranksPageSize')
        c.pageCount = int(math.ceil(len(items) / float(c.pageSize)))
        c.currentPage = page
        c.userItems = items[offset:offset + c.pageSize]
        
        #Default images
        c.defaultArtistImage = GlobalConfig.get('popcard.default.images.artist.small').value
        
        return render('/widget/media/music/ranks.mako')
