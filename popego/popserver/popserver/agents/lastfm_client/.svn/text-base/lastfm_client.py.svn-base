# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import logging
import string
import urllib2, urllib
import xml.dom.minidom
from datetime import datetime

def innertext(dom_node):
    """ algo así como innerHTML :) """
    textNode = dom_node.firstChild
    return textNode.nodeValue if (textNode is not None and textNode.nodeType == 3) else ''

def firstnode(dom_node, tag):
    """ primer child de ``dom_node`` con tag ``tag`` """
    f = dom_node.getElementsByTagName(tag)
    return f[0] if len(f) > 0 else None

tagmapper = lambda t: innertext(firstnode(t, 'name'))

log = logging.getLogger(__name__)

class LastFMClientException(Exception): pass
class LastFMClientItemNotFoundException(Exception): pass


# Hay bastante duplicacion, podría haberse hecho mejor...prometo refactoring :)

class LastFMClient:
    
    API_URL = 'http://ws.audioscrobbler.com/1.0'

    def __init__(self):
        self._cache = {}


    def userExists(self, username):
        try:
            self._getFeed('%s/user/%s/profile.xml' % (LastFMClient.API_URL, self._q(username)))
        except LastFMClientItemNotFoundException:
            return False

        return True
        

    def getRecentTracksForUser(self, username):
        """ Obtener la lista de pistas recientemente escuchadas por ``username`` """
        parsedFeed = self._getFeed('%s/user/%s/recenttracks.xml' % (LastFMClient.API_URL, self._q(username)))
        return map(lambda n: { 'artist': innertext(firstnode(n, 'artist')),
                               'artist_mbid': firstnode(n, 'artist').attributes.get('mbid').value,
                               'name': innertext(firstnode(n, 'name')),
                               'album': innertext(firstnode(n, 'album')),
                               'url': innertext(firstnode(n, 'url')),
                               'creation_date': datetime.utcfromtimestamp(int(firstnode(n, 'date').attributes.get('uts').value)) },
                   parsedFeed.getElementsByTagName('recenttracks')[0].getElementsByTagName('track'))

    def getTopTracksForUser(self, username):
        """ Obtener los tracks favoritos de ``username`` """
        # http://ws.audioscrobbler.com/1.0/user/RJ/toptracks.xml
        parsedFeed = self._getFeed('%s/user/%s/toptracks.xml' % (LastFMClient.API_URL, self._q(username)))
        return map(lambda n: { 'artist': innertext(firstnode(n, 'artist')),
                               'artist_mbid': firstnode(n, 'artist').attributes.get('mbid').value,
                               'name': innertext(firstnode(n, 'name')),
                               'url': innertext(firstnode(n, 'url')),
                               'playcount': int(innertext(firstnode(n, 'playcount'))) },
                   parsedFeed.getElementsByTagName('toptracks')[0].getElementsByTagName('track'))
        

    def getTopArtistsForUser(self, username):
        """ Lista de artistas favoritos de ``username`` """
        parsedFeed = self._getFeed('%s/user/%s/topartists.xml' % (LastFMClient.API_URL, self._q(username)))
        return map(lambda n: { 'name': innertext(firstnode(n, 'name')),
                               'mbid': innertext(firstnode(n, 'mbid')),
                               'url': innertext(firstnode(n, 'url')),
                               'thumbnail': innertext(firstnode(n, 'thumbnail')),
                               'image': innertext(firstnode(n, 'image')),
                               'playcount': int(innertext(firstnode(n, 'playcount')))},
                   parsedFeed.getElementsByTagName('topartists')[0].getElementsByTagName('artist'))

    def getUserTagsForTrack(self, username, track_artist, track_name):
        """ Lista de tags aplicadas por ``username`` al track definido por ``track_artist`` y ``track_name`` """
        parsedFeed = self._getFeed('%s/user/%s/tracktags.xml?%s' % (LastFMClient.API_URL, 
                                                                     self._q(username), 
                                                                     urllib.urlencode([('artist', track_artist.encode('utf-8')), ('track', track_name.encode('utf-8'))])))
        return map(tagmapper,
                   firstnode(parsedFeed, 'tracktags').getElementsByTagName('tag') or [])

    def getUserTagsForArtist(self, username, artist):
        """ Lista de tags aplicadas por ``username`` a ``artist`` """
        parsedFeed = self._getFeed('%s/user/%s/artisttags.xml?%s' % (LastFMClient.API_URL, 
                                                                     self._q(username), 
                                                                     urllib.urlencode([('artist', artist.encode('utf-8'))])))
        return map(tagmapper,
                   (lambda node: node is not None and node.getElementsByTagName('tag') or [])(firstnode(parsedFeed, 'artisttags')))


    def getTopTagsForTrack(self, track_artist, track_name):
        """ Lista de top tags para el track definido por ``track_artist`` y ``track_name`` """
        parsedFeed = self._getFeed('%s/track/%s/%s/toptags.xml' % (LastFMClient.API_URL, 
                                                                     self._q(track_artist), 
                                                                     self._q(track_name)))
        return map(tagmapper,
                   (lambda node: node is not None and node.getElementsByTagName('tag') or [])(firstnode(parsedFeed, 'artisttags')))

    def getTopTagsForArtist(self, artist):
        """ Lista de top tags para ``artist`` """
        parsedFeed = self._getFeed('%s/artist/%s/toptags.xml' % (LastFMClient.API_URL, 
                                                                 self._q(artist)))
        return map(tagmapper,
                   firstnode(parsedFeed, 'toptags').getElementsByTagName('tag'))


    def getAlbum(self, album_artist, album_name):
        """ Obtiene informacion sobre el album ``album_name`` de ``album_artist`` """
        parsedFeed = self._getFeed('%s/album/%s/%s/info.xml' % (LastFMClient.API_URL,
                                                                self._q(album_artist),
                                                                self._q(album_name)))
        
        albumData = {}
        rootNode = firstnode(parsedFeed, 'album')
        
        albumData['artist'] = rootNode.attributes.get('artist').value
        albumData['title'] = rootNode.attributes.get('title').value
        albumData['url'] = innertext(firstnode(rootNode, 'url'))
        albumData['images'] = {}
        
        albumData['images'].update(
            map(lambda n: (n.nodeName, innertext(n)),
                filter(lambda n: n.nodeName in ['small', 'medium', 'large'], firstnode(rootNode, 'coverart').childNodes))
            )

        albumData['tracks'] = map(lambda n: n.attributes.get('title').value, firstnode(rootNode, 'tracks').getElementsByTagName('track'))

        return albumData

    def getArtistData(self, artist):
        """ Retorna un diccionario con el URL de la foto del artista y su mbid (id en musicbrainz) """
        # http://ws.audioscrobbler.com/1.0/artist/Metallica/similar.xml
        parsedFeed = self._getFeed('%s/artist/%s/similar.xml' % (LastFMClient.API_URL,
                                                                self._q(artist)))

        rootNode = firstnode(parsedFeed, 'similarartists')
        
        pic = rootNode.attributes.get('picture').value
        
        # si me retorna el 'placeholder' image, no la quiero
        if string.rfind(pic, 'noimage') != -1: pic = None

        return { 'name': artist,
                 'image': pic,
                 'mbid': rootNode.attributes.get('mbid').value,
                 'url' : 'http://last.fm/music/%s' % self._q(artist) } 

    def _q(self, str):
        return urllib2.quote(urllib.quote_plus(str.encode('utf_8')))

    def _getFeed(self, url):
        """ Realiza un pedido al endpoint de Last.fm y retorna el resultado del parseo con minidom """
        #print url
        
        if url in self._cache:
            return self._cache[url]
        try:
            feed = urllib2.urlopen(url)
            self._cache[url] = xml.dom.minidom.parseString(feed.read())
        except urllib2.HTTPError:
            raise LastFMClientItemNotFoundException, "Request to '%s' returned a 404" % url
        except IOError:
            # no se pudo leer el stream
            raise LastFMClientException, "Can't read stream from the webservice"
        except xml.parsers.expat.ExpatError:
            # audioscrobbler nos dió XML mal formado
            raise LastFMClientException, "Can't parse response from the webservice"
        except:
            raise LastFMClientException, "Unknown error"
        
        return self._cache[url]

