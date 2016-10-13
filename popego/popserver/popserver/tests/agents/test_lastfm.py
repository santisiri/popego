# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.tests.nodb_model import *
from popserver.tests import *
from fixture import DataTestCase
from popserver.tests import popfixtures
from popserver.agents.lastfm_agent import LastFmAgent
from popserver.agents.lastfm_client import LastFMClient
import popserver.agents
import types
import unittest

class TestLastFmClient(unittest.TestCase):
    def setUp(self):
        self._restoreMethod = popserver.agents.lastfm_client.LastFMClient._getFeed
        LastFMClient._getFeed = types.MethodType(mock_lastfm_getFeed, None, LastFMClient)
        self.client = LastFMClient()

    def tearDown(self):
        LastFMClient._getFeed = types.MethodType(self._restoreMethod, None, LastFMClient)


    def testRecentTracks(self):
        t = self.client.getRecentTracksForUser('maristaran')
        assert type(t) == type([])
        assert len(t) == 1
        assert type(t[0]) == type({})
        assert t[0]['artist'] == 'Willie Bobo'

    def testTopTracks(self):
        t = self.client.getTopTracksForUser('maristaran')
        assert type(t) == type([])
        assert len(t) == 1
        assert type(t[0]) == type({})
        assert t[0]['artist'] == 'Brian Wilson'
        assert t[0]['name'] == 'Our Prayer Gee'

    def testTopArtists(self):
        t = self.client.getTopArtistsForUser('maristaran')
        assert type(t) == type([])
        assert len(t) == 1
        assert type(t[0]) == type({})
        assert t[0]['name'] == 'The Beatles'

    def testUserTagsForTrack(self):
        t = self.client.getUserTagsForTrack('maristaran', 'Brian Wilson', 'Our Prayer Gee')
        assert type(t) == type([])
        assert len(t) == 1
        assert t == ['bombastic']

    def testTopArtistsForUser(self):
        t = self.client.getTopArtistsForUser('maristaran')
        assert type(t) == type([])
        assert len(t) == 1
        assert t[0]['name'] == 'The Beatles'
        
    def testTopTagsForTrack(self):
        t = self.client.getTopTagsForTrack('Willie Bobo', 'Funky Sneakers')
        assert type(t) == type([])
        assert len(t) == 0

    def testGetArtistData(self):
        t = self.client.getArtistData('Brian Wilson')
        assert type(t) == type({})
        assert t['name'] == 'Brian Wilson'


# TODO: tests para el agente

# class TestLastFmAgent(TestModel, DataTestCase):

#     fixture = dbfixture
#     datasets = [popfixtures.UserData, popfixtures.ServiceTypeData, popfixtures.ServiceData, popfixtures.AccountData]

#     def setUp(self):
#         TestModel.setUp(self)
#         DataTestCase.setUp(self)
#         self._restoreMethod = popserver.agents.lastfm_client.LastFMClient._getFeed

#         LastFMClient._getFeed = types.MethodType(mock_lastfm_getFeed, None, LastFMClient)        
#         self.agent = LastFmAgent()

#         self.user = self.data.UserData.dartagnan
#         self.lastfm_svc = self.data.ServiceData.lastfm
#         self.account = Account.get_by(user_id=self.user.id, service_id=self.lastfm_svc.id)

#     def tearDown(self):
#         dbsession.clear()
#         DataTestCase.tearDown(self)
#         TestModel.tearDown(self)
#         LastFMClient._getFeed = types.MethodType(self._restoreMethod, None, LastFMClient)

#     def test_getUserGraph(self):
#         r = self.agent.getUserGraph(self.account)
#         assert len(r) == 3 # grupos: top artists, top tracks y recently_listened
#         assert map(type, r) == [popserver.model.ItemGroup, popserver.model.ItemGroup, popserver.model.ItemGroup]
#         assert map(lambda g: type(g.items[0]), r) == [popserver.model.UserItem, popserver.model.UserItem,popserver.model.UserItem]
#         assert map(lambda g: len(g.items), r) == [1, 1, 1]
        
#         top_artists = r[0]
#         assert type(top_artists.items[0].item) == popserver.model.Artist
#         assert top_artists.items[0].item.title == 'The Beatles'

#         top_tracks = r[1]
#         assert type(top_tracks.items[0].item) == popserver.model.Song
#         assert top_tracks.items[0].item.title == 'Our Prayer Gee'
#         assert top_tracks.items[0].item.artist.title == 'Brian Wilson'

#         recently_listened = r[2]
#         assert type(recently_listened.items[0].item) == popserver.model.Song
#         assert recently_listened.items[0].item.title == 'Funky Sneakers'
#         assert recently_listened.items[0].item.artist.title == 'Willie Bobo'
#         assert True

        


def mock_lastfm_getFeed(self, url):
    samples = {
        'http://ws.audioscrobbler.com/1.0/user/maristaran/recenttracks.xml' : 'recenttracks.xml',
        'http://ws.audioscrobbler.com/1.0/artist/Willie%2BBobo/similar.xml' : 'willie-bobo-similar.xml',
        'http://ws.audioscrobbler.com/1.0/track/Willie%2BBobo/Funky%2BSneakers/toptags.xml' : 'funky-sneakers-toptags.xml',
        'http://ws.audioscrobbler.com/1.0/user/maristaran/tracktags.xml?artist=Willie+Bobo&track=Funky+Sneakers' : 'funky-sneakers-tracktags.xml',
        'http://ws.audioscrobbler.com/1.0/user/maristaran/toptracks.xml' : 'toptracks.xml',
        'http://ws.audioscrobbler.com/1.0/artist/Brian%2BWilson/similar.xml' : 'brian-wilson-similar.xml',
        'http://ws.audioscrobbler.com/1.0/track/Brian%2BWilson/Our%2BPrayer%2BGee/toptags.xml' : 'our-prayer-gee-toptags.xml',
        'http://ws.audioscrobbler.com/1.0/user/maristaran/tracktags.xml?artist=Brian+Wilson&track=Our+Prayer+Gee' : 'maristaran-our-prayer-gee-toptags.xml',
        'http://ws.audioscrobbler.com/1.0/user/maristaran/topartists.xml' : 'topartists.xml',
        'http://ws.audioscrobbler.com/1.0/artist/The%2BBeatles/similar.xml' : 'beatles-similar.xml',
        'http://ws.audioscrobbler.com/1.0/user/maristaran/artisttags.xml?artist=The+Beatles' : 'maristaran-beatles-tags.xml'
       
    }
    import xml.dom.minidom
    if samples[url] == 404:
        import urllib2
        raise urllib2.HTTPError
    else:
        return xml.dom.minidom.parse(popserver.tests.__path__[0] + '/samples/lastfm/' + samples[url])


# class TestLastfmAgent(DataTestCase, TestModel):
#     fixture = dbfixture
#     datasets = [popfixtures.UserData, popfixtures.ServiceTypeData, popfixtures.ServiceData, popfixtures.AccountData]
    
#     def setUp(self):
#         TestModel.setUp(self)
#         DataTestCase.setUp(self)
#         self.user = User.get_by(username='darty')
#         self.lastfm_svc = Service.get_by(name='Last.FM')
#         self.account = Account.get_by(user=self.user, service=self.lastfm_svc)
        

#         self.agent = self.lastfm_svc.getAgent()

#     def tearDown(self):
#         DataTestCase.tearDown(self)
#         TestModel.tearDown(self)
#         LastFmAgent._getFeed = orig_getFeed


    
