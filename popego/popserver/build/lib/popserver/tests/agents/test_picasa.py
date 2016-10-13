from unittest import TestCase
import datetime
import popserver.tests.mock as p
from popserver.agents import picasa_agent as pi
from gdata import BatchFeedFromString
from popserver.tests.nodb_model import Account

class TestPicasaAgent(TestCase):
    def setUp(self):
        self.account = Account(username='mcortesi')
        self.cliMock = p.Mock()
        self.originalCli = pi.cli
        pi.cli = self.cliMock

    def tearDown(self):
        pi.cli = self.originalCli


    def test_parseUserGroupsFeed(self):
        self._mockFeedCall('user_feed')

        plEntries = list(pi.iUserGroupsEntries(self.account.username))

        self.assertEqual(len(plEntries),4)
        pls = map(pi.entry2group, plEntries)

        # first from playlists
        extId, name = pls[0]
        self.assertEqual(name,"Viaje a Arrail D'Ajuda")
        self.assertEqual(extId, 
                 'http://picasaweb.google.com/data/feed/api/user/mcortesi/albumid/5162534524685921441')

        self.cliMock.verify()

    def test_getGroupsToCheck_NewAccount(self):
        self._mockFeedCall('user_feed')
        newGroups, changedGroups = pi.getGroupsToCheck('mcortesi',None)
        assert len(changedGroups) == 0
        assert len(newGroups) == 4
        
        for g in newGroups:
            assert isinstance(g, tuple)
            assert len(g) == 2

        self.cliMock.verify()

    def test_getGroupsToCheck_OldAccount(self):
        self._mockFeedCall('user_feed')
        aDate = datetime.datetime(2007,1,1)
        newGroups, changedGroups = pi.getGroupsToCheck('mcortesi', aDate)
        
        self.assertEqual(len(newGroups), 2)
        self.assertEqual(len(changedGroups), 2)

        for g in newGroups:
            assert isinstance(g, tuple)
            assert len(g) == 2

        for g in changedGroups:
            assert isinstance(g, str)

        self.cliMock.verify()

    def test_iGroupEntries_allPages(self):
        url = self._mockFeedCall('album_feed','blabla')
        
        entries = list(pi.iGroupEntries(url))

        assert len(entries) == 126
        self.cliMock.verify()

    def test_itemAttrs(self):
        url = self._mockFeedCall('album_feed','blabla')
        firstEntry = pi.iGroupEntries(url).next()
        attrs = pi.itemAttrs(firstEntry)

        date = datetime.datetime(2008,02,02,23,50,51)
        self.assertEqual(attrs['creation_date'], date)
        self.assertEquals(attrs['title'], 'P1000056.JPG')
        self.assertEquals(attrs['description'], 'Llegamos!')
        self.assertEquals(attrs['external_url'], 'http://picasaweb.google.com/lh/photo/K3RuGPLIpryDd6KXUnZ5gA')
        self.assertEquals(attrs['thumbnail_url'],'http://lh5.google.com/mcortesi/R6UB20SYLLI/AAAAAAAAA3o/n_7Zjx7_aWM/s144/P1000056.JPG')
        
        self.cliMock.verify()

#     def test_updateAccount_NewAccount(self):
#         self._mockFeedCall('playlists','playlists-empty')
#         self._mockFeedCall('favorites','favorites')
#         self._mockFeedCall('favorites?start-index=26','favorites')        
#         self._mockFeedCall('uploads','favorites')
#         self._mockFeedCall('uploads?start-index=26','favorites')        

#         cacheApi = p.Mock()
#         cacheApi.expects(p.exactly(2)).method('addGroup')
#         cacheApi.expects(p.exactly(100)).method('itemExists').will(p.return_value(False))
#         cacheApi.expects(p.exactly(100)).method('addItem')
#         cacheApi.expects(p.exactly(100)).method('bindItem2Group')

#         pi.updateAccount(self.account, cacheApi)

#         cacheApi.verify()
#         self.cliMock.verify()

#     def test_updateAccount_OldAccount(self):
#         self._mockFeedCall('playlists','playlists-empty')
#         self._mockFeedCall('favorites','favorites')
#         self._mockFeedCall('uploads','favorites')

#         self.account.last_updated = datetime.datetime(2007,5,1)
        
#         cacheApi = p.Mock()
#         cacheApi.expects(p.exactly(2)).method('groupItems').will(p.return_value(
#                 ['http://www.youtube.com/watch?v=i_QABS88nDc']))
#         cacheApi.expects(p.exactly(14)).method('itemExists').will(p.return_value(False))
#         cacheApi.expects(p.exactly(14)).method('addItem')
#         cacheApi.expects(p.exactly(14)).method('bindItem2Group')


#         pi.updateAccount(self.account, cacheApi)

#         cacheApi.verify()
#         self.cliMock.verify()
        
    def _mockFeedCall(self, filename, albumId=None):
        feedUrl = pi.feedUrl(self.account.username, albumId)
        feed = self._getFeed(filename)
        self.cliMock.expects(p.once()).GetFeed(p.eq(feedUrl)).will(p.return_value(feed))
        return feedUrl


    def _getFeed(self, filename):
        import popserver.tests as t
        self.samplesPath = t.__path__[0] + '/samples/picasa/'
        f = open(self.samplesPath + filename)
        feed = BatchFeedFromString(f.read())
        f.close()
        return feed

