# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import logging

from string import lower, replace
from popserver.agents.lastfm_client import LastFMClient, LastFMClientException, LastFMClientItemNotFoundException
from popserver.lib.functional import retry

log = logging.getLogger(__name__)


class LastFmAgent:

    NUM_ITEMS = 10 # cuántos items queremos traer

    def __init__(self):
        self.client = LastFMClient()

    def accountHome(self, account):
        return "http://www.last.fm/user/%s/" % account.username

    def updateAccount(self, account, cacheApi):
        if account.home_url is None:
            account.home_url = self.accountHome(account)

        self._createDefaultGroups(cacheApi)
        self._updateRecentTracks(account, cacheApi)
        self._updateTopTracks(account, cacheApi)
        self._updateTopArtists(account, cacheApi)

    def userExists(self, username):
        return self.client.userExists(username)

    @retry(1, LastFMClientException, LastFMClientItemNotFoundException)
    def getUserTagsFromTrack(username, artist, songTitle):
        return self.client.getUserTagsForTrack(username, artist, songTitle)        

    def _updateRecentTracks(self, account, cacheApi):
        """ Actualiza los Recent Tracks del usuario """
        recent_tracks = self.client.getRecentTracksForUser(account.username)
        if (len(recent_tracks) > 0) \
                and (account.last_updated is not None) \
                and (recent_tracks[0]['creation_date'] < account.last_updated): 
            return
 
        # limpiar el group recently_listened
        map(lambda it: cacheApi.removeItemFromGroup('recently_listened', it), cacheApi.groupItems('recently_listened'))

        ids = []
        for track in recent_tracks[:LastFmAgent.NUM_ITEMS]:
            song = self._songAttrs(track)
            song_id = song['external_id']

            # avoid dups
            if song_id in ids:
                continue
            ids.append(song_id)
            
            # si el Song no tiene tags, ni nos molestamos en buscar los tags que creo el usuario 
            if len(song['item_tags']) > 0:
                song['user_tags'] = self.getUserTagsFromTrack(account.username, song['artist']['title'], song['title'])

            song['creation_date'] = track['creation_date']

            if not cacheApi.itemExists(song_id):
                cacheApi.addItem(song_id, song)
            cacheApi.bindItem2Group('recently_listened', song_id)
 

    def _updateTopTracks(self, account, cacheApi):
        map(lambda it: cacheApi.removeItemFromGroup('top_tracks', it), cacheApi.groupItems('top_tracks'))
        top_tracks = self.client.getTopTracksForUser(account.username)
        i = 0
        
        while i < LastFmAgent.NUM_ITEMS and i < len(top_tracks):
            t = top_tracks[i]
            i += 1

            song = self._songAttrs(t)
            
            song_id = song['external_id']
            song['user_tags'] = self.client.getUserTagsForTrack(account.username, song['artist']['title'], song['title']) if len(song['item_tags']) > 0 else []
            song['playcount'] = t['playcount']

            if not cacheApi.itemExists(song_id):
                cacheApi.addItem(song_id, song)
            
            cacheApi.bindItem2Group('top_tracks', song_id)

    def _updateTopArtists(self, account, cacheApi):
        map(lambda it: cacheApi.removeItemFromGroup('top_artists', it), cacheApi.groupItems('top_artists'))
        top_artists = self.client.getTopArtistsForUser(account.username)
        i = 0
        while i < LastFmAgent.NUM_ITEMS and i < len(top_artists):
            t = top_artists[i]
            i += 1

            artist = self._artistAttrs(t['name'])
            artist_id = artist['external_id']
            artist['user_tags'] = self.client.getUserTagsForArtist(account.username, artist['title']) if len(artist['item_tags']) > 0 else []
            artist['playcount'] = t['playcount']

            if not cacheApi.itemExists(artist_id):
                cacheApi.addItem(artist_id, artist)
            
            cacheApi.bindItem2Group('top_artists', artist_id)


    def _createDefaultGroups(self, cacheApi):
        """ Crea los ItemGroup por omisión para Last.FM: Recently Played, Top Artists, Top Tracks """
        for g in ['Recently Listened', 'Top Artists', 'Top Tracks']:
            gid = replace(lower(g), ' ', '_')
            if not cacheApi.groupExists(gid):
                cacheApi.addGroup(gid, name=g, is_null_group=False)
                                                             

    def _songAttrs(self, track_data):
        """ Retorna una tupla: (song_extrenal_id, song_attrs) """
        return  { 'title' : track_data['name'],
                  'external_id' : track_data['url'],
                  'artist' : self._artistAttrs(track_data['artist']),
                  'item_tags' : self.client.getTopTagsForTrack(track_data['artist'], track_data['name']) }

    def _artistAttrs(self, artist_name):
        artist_data = self.client.getArtistData(artist_name)
        e_id = artist_data['name']
        if artist_data['mbid'] not in (None, ''): e_id = 'mbid-%s' % artist_data['mbid']

        return { 'title' : artist_data['name'],
                 'photo_url' : artist_data['image'],
                 'external_id' : e_id,
                 'url' : artist_data['url'],
                 'item_tags' : self.client.getTopTagsForArtist(artist_data['name']) }
