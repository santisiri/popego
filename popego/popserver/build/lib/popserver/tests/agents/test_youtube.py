from popserver.tests.nodb_model import *
from popserver.tests import *
import datetime
import popserver.tests.mock as p
from popserver.agents import youtube_agent as yt
from gdata import BatchFeedFromString
from unittest import TestCase

class TestYoutubeAgent(TestCase):
    def setUp(self):
        super(self.__class__,self).setUp()
        self.account = Account(username='santisiri')
        self.cliMock = p.Mock()
        self.originalCli = yt.cli
        yt.cli = self.cliMock

    def tearDown(self):
        yt.cli = self.originalCli
        super(self.__class__,self).tearDown()

    def test_parsePlaylistFeed(self):
        self._mockFeedCall('playlists','playlists')

        plEntries = list(yt.iPlaylistEntries(self.account.username))

        self.assertEqual(len(plEntries),13)
        pls = map(yt.entry2group, plEntries)

        # first from playlists
        extId, name = pls[0]
        self.assertEqual(name,"Ads")
        self.assertEqual(extId, 
                 'http://gdata.youtube.com/feeds/playlists/FFF43205215330C')

        self.cliMock.verify()

    def test_getDefaultGroups(self):
        groups = yt.getDefaultGroups('santisiri')
        assert len(groups) == 2
        for g in groups:
            assert isinstance(g, tuple)
            assert len(g) == 2

    def test_getGroupsToCheck_NewAccount(self):
        self._mockFeedCall('playlists','playlists')
        newGroups, changedGroups = yt.getGroupsToCheck('santisiri',None)
        assert len(changedGroups) == 0
        assert len(newGroups) == 15
        
        for g in newGroups:
            assert isinstance(g, tuple)
            assert len(g) == 2

        self.cliMock.verify()

    def test_getGroupsToCheck_OldAccount(self):
        self._mockFeedCall('playlists','playlists')
        aDate = datetime.datetime(2007,5,1)
        newGroups, changedGroups = yt.getGroupsToCheck('santisiri', aDate)
        
        self.assertEqual(len(newGroups), 1)
        self.assertEqual(len(changedGroups), 7)

        for g in newGroups:
            assert isinstance(g, tuple)
            assert len(g) == 2

        for g in changedGroups:
            assert isinstance(g, str)

        self.cliMock.verify()

    def test_iGroupEntries_allPages(self):
        self._mockFeedCall('favorites','favorites')
        self._mockFeedCall('favorites?start-index=26','favorites')        
        
        favId = yt.getDefaultGroups(self.account.username)[0][0]
        entries = list(yt.iGroupEntries(favId))

        assert len(entries) == 50
        self.cliMock.verify()

    def test_itemAttrs(self):
        self._mockFeedCall('favorites','favorites')
        favId = yt.getDefaultGroups(self.account.username)[0][0]
        firstEntry = yt.iGroupEntries(favId).next()

        attrs = yt.itemAttrs(firstEntry)


        date = datetime.datetime(2007,11,21,0,38,29)
        self.assertEqual(attrs['creation_date'], date)
        self.assertEquals(attrs['title'], 'Pole Position Commercial! (Atari)')
        self.assertEquals(attrs['description'],
                          'Xbox and Playstation commercials have got nuthin\' on this old classic. Even the theme song rocks!')
        self.assertEquals(attrs['embedURL'],'http://www.youtube.com/v/Om84Zc4-KcQ')
        self.assertEquals(attrs['externalURL'], 'http://www.youtube.com/watch?v=Om84Zc4-KcQ')
        self.assertEquals(len(attrs['thumbnails']),3)
        
        th = attrs['thumbnails'][0]
        self.assertEquals(th['width'],130)
        self.assertEquals(th['height'],97)
        assert th['time'] in ['00:00:45.500','00:00:22.750','00:01:08.250']

        self.cliMock.verify()

    def test_updateAccount_NewAccount(self):
        self._mockFeedCall('playlists','playlists-empty')
        self._mockFeedCall('favorites','favorites')
        self._mockFeedCall('favorites?start-index=26','favorites')        
        self._mockFeedCall('uploads','favorites')
        self._mockFeedCall('uploads?start-index=26','favorites')        

        cacheApi = p.Mock()
        cacheApi.expects(p.exactly(2)).method('addGroup')
        cacheApi.expects(p.exactly(100)).method('itemExists').will(p.return_value(False))
        cacheApi.expects(p.exactly(100)).method('addItem')
        cacheApi.expects(p.exactly(100)).method('bindItem2Group')

        yt.updateAccount(self.account, cacheApi)

        cacheApi.verify()
        self.cliMock.verify()

    def test_updateAccount_OldAccount(self):
        self._mockFeedCall('playlists','playlists-empty')
        self._mockFeedCall('favorites','favorites')
        self._mockFeedCall('favorites?start-index=26','favorites')        
        self._mockFeedCall('uploads','favorites')
        self._mockFeedCall('uploads?start-index=26','favorites')        

        self.account.last_updated = datetime.datetime(2007,5,1)

        cacheApi = p.Mock()
        cacheApi.expects(p.exactly(2)).method('groupItems').will(p.return_value(
                ['http://www.youtube.com/watch?v=i_QABS88nDc']))

        cacheApi.expects(p.exactly(2)).method('removeItemFromGroup')
        cacheApi.expects(p.exactly(100)).method('itemExists').will(p.return_value(False))
        cacheApi.expects(p.exactly(100)).method('addItem')
        cacheApi.expects(p.exactly(100)).method('bindItem2Group')

        yt.updateAccount(self.account, cacheApi)

        cacheApi.verify()
        self.cliMock.verify()

    def _mockFeedCall(self, feedName,filename):
        feedUrl = 'http://gdata.youtube.com/feeds/users/%s/%s' % (self.account.username, feedName)
        feed = self._getFeed(filename)
        return self.cliMock.expects(p.once()).GetFeed(p.eq(feedUrl)).will(p.return_value(feed))




    def _getFeed(self, filename):
        import popserver.tests as t
        self.samplesPath = t.__path__[0] + '/samples/youtube/'        
        f = open(self.samplesPath + filename)
        feed = BatchFeedFromString(f.read())
        f.close()
        return feed

