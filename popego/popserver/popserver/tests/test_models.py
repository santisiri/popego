# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.model import *
from popserver.tests import *
from fixture import DataTestCase
import popfixtures
import popserver.agents as agents

class TestUsers(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)
   
    def test_dartagnanHasAnEmail(self):
        assert self.data.UserData.dartagnan.email == 'dartagnan@mousquetaires.fr'

class TestServices(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.ServiceTypeData, 
                popfixtures.ServiceData, 
                popfixtures.AccountData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)
    
    def test_getAgent(self):
        agent = Service.get_by(name='Flickr').getAgent()
        assert isinstance(agent, agents.flickr_agent.FlickrAgent)
        agent = Service.get_by(name='YouTube').getAgent()
        assert agent is agents.youtube_agent
        agent = Service.get_by(name='del.icio.us').getAgent()
        assert agent is agents.delicious_agent
        agent = Service.get_by(name='Last.FM').getAgent()
        assert isinstance(agent, agents.lastfm_agent.LastFmAgent)

    def test_getUserServicesByType(self):
        aramis = User.get_by(username='aramis')
        photos_service_type = ServiceType.get_by(type='photos')
        photo_services = photos_service_type.services
        
    def test_serviceFaviconURL(self):
        flickr = Service.get_by(name='Flickr')
        assert flickr.faviconURL() == '/images/icons/flickr_favicon.png'

class TestServiceTypes(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.ServiceTypeData, 
                popfixtures.ServiceData, 
                popfixtures.AccountData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)
    
    def test_getUserServicesByType(self):
        aramis_services = ServiceType.get_by(type='photos').getServicesForUser(User.get_by(username='aramis'))
        assert type(aramis_services) == type([])
        assert len(aramis_services) == 1
        assert aramis_services[0] == Service.get_by(name='PicasaWeb')

        darty_services = ServiceType.get_by(type='photos').getServicesForUser(User.get_by(username='darty'))
        assert type(darty_services) == type([])
        assert len(darty_services) == 1
        assert darty_services[0] == Service.get_by(name='Flickr')

class TestTagging(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.ServiceTypeData, 
                popfixtures.ServiceData, 
                popfixtures.AccountData,
                popfixtures.ItemGroupData,
                popfixtures.UserItemData,
                popfixtures.VideoData,
                popfixtures.BookmarkData,
                popfixtures.TagData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)

    def test_tagsItem(self):
        t = Tag.get_by(name='foo')
        assert len(t.items) == 1
        t.items[0] == Video.get(1)

    def test_itemTags(self):
        i = Video.get(1)
        assert i.title == 'title_yt_v1'
        assert len(i.tags) == 3
        assert map(lambda t: t.name, i.tags) == ['bar', 'baz', 'foo']

    def test_userItemTags(self):
        aramis_delicious = Account.query.filter_by(user_id=User.get_by(username='aramis').id, service_id=Service.get_by(name='del.icio.us').id).one()
        darty_delicious = Account.query.filter_by(user_id=User.get_by(username='darty').id, service_id=Service.get_by(name='del.icio.us').id).one()

        assert len(darty_delicious.item_groups[0].items[0].tags) == 1
        assert darty_delicious.item_groups[0].items[0].tags[0].name == 'foo'

        assert len(aramis_delicious.item_groups[0].items[0].tags) == 1
        assert aramis_delicious.item_groups[0].items[0].tags[0].name == 'bar'

    def test_emptyUserItemTagsDelegatesToItem(self):
        video_useritem = UserItem.get(6)
        assert video_useritem._tags == []

        assert video_useritem.tags == video_useritem.item.tags

    def test_addTags(self):
        v = Video.get(1)
        assert len(v.tags) == 3
        v.addTags(['a', 'b', 'c'])
        assert len(v.tags) == 6
        


class TestDeletes(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.ServiceTypeData, 
                popfixtures.ServiceData, 
                popfixtures.AccountData,
                popfixtures.ItemGroupData,
                popfixtures.UserItemData,
                popfixtures.VideoData,
                popfixtures.BookmarkData,
                popfixtures.TagData,
                popfixtures.ArtistUserItemData,
                popfixtures.ArtistData,
                popfixtures.SongData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        dbsession.clear()
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)

    def _checkPostDeleteAssertions(self):
        aramis = User.get_by(username='aramis')
        assert len(aramis.accounts) == 1
        assert aramis.accounts[0].service.name == 'PicasaWeb'
        assert ItemGroup.query.filter(ItemGroup.account.has(Account.user_id==aramis.id)).count() == 0
        assert UserItem.query.filter_by(user=aramis).count() == 0

    def test_removeAccount(self):
        self._removeAccount()
        self._checkPostDeleteAssertions()
        
    def test_removeOrphanAccount(self):
        aramis = User.get_by(username='aramis')
        assert ItemGroup.query.filter(ItemGroup.account.has(Account.user==aramis)).count() == 1
        for i in range(len(aramis.accounts)):
            if aramis.accounts[i].service.name == 'del.icio.us':
                del(aramis.accounts[i])
                break
        dbsession.flush()
        self._checkPostDeleteAssertions()

    def _removeAccount(self):
        aramis = User.get_by(username='aramis')
        account = Account.query.filter(Account.user == aramis).filter(Account.service.has(Service.name == 'del.icio.us')).one()
        assert ItemGroup.query.filter(ItemGroup.account.has(Account.user_id == aramis.id)).count() == 1
        account.delete()
        dbsession.flush()


    def test_orphanUserItems(self):
        self._removeAccount()
        aramis = User.get_by(username='aramis')
        assert UserItem.query.filter_by(user=aramis).filter(UserItem.item.has(Item.row_type=='bookmark')).count() == 0
        assert aramis.weightedObjCount == 0


    def test_tagcountRemovalWhenUserItemTagRemoved(self):
        aramis = User.get_by(username='aramis')
        assert TagCount.query.filter_by(user=aramis).count() == 1
        self._removeAccount()
        aramis = User.get_by(username='aramis')
        assert TagCount.query.filter_by(user=aramis).count() == 0


    def test_tagcountRemovalWhenItemTagRemoved(self):
        phillipe = User.get_by(username='phillipe')
        assert TagCount.query.filter_by(user=phillipe).count() == 3
        account = Account.query.filter(Account.user == phillipe) \
            .filter(Account.service.has(Service.name == 'YouTube')).one()
        assert ItemGroup.query.join('account') \
            .filter(Account.user_id == phillipe.id) \
            .filter(Account.service.has(Service.name == 'YouTube')).count() == 1
        account.delete()
        dbsession.flush()
        phillipe = User.get_by(username='phillipe')
        assert TagCount.query.filter_by(user=phillipe).count() == 0

    def test_artistRemovalWhenSongIsReferencing(self):
        phillipe = User.get_by(username='phillipe')
        lastfmAccount = Account.query.filter(Account.user == phillipe) \
            .filter(Account.service.has(Service.name == 'Last.FM')).one()
        assert Artist.query.count() == 1
        assert Song.query.count() == 1

        lastfmAccount.delete()
        dbsession.flush()

        assert Account.query.filter(Account.user == phillipe) \
          .filter(Account.service.has(Service.name == 'Last.FM')).count() == 0
        assert Artist.query.count() == 0
        assert Song.query.count() == 0 


    
from popserver.ai.interest import tag

class TestTagInterests(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.TagData,
                popfixtures.GlobalConfigData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)
        
        # a darty y phillipe les interesa 'foo'
        tag.setInterestUp(TagCount.get_by(user_id=self.data.UserData.dartagnan.id, tag_id=self.data.TagData.foo.id))
        tag.setInterestUp(TagCount.get_by(user_id=self.data.UserData.phillipe.id, tag_id=self.data.TagData.foo.id))
        # a aramis tambien le interesa 'bar'
        tag.setInterestUp(TagCount.get_by(user_id=self.data.UserData.aramis.id, tag_id=self.data.TagData.bar.id))

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)

    def test_isInterest(self):
        # es un interest para el threshold default (4)
        assert tag.isInterest('foo')

        # bar (solo 'interesantizado' por aramis) no es un interest
        assert not tag.isInterest('bar')

    def test_tagPromotion(self):
        # un tag que no era Interest, pasa a serlo después de una acción de usuario
        assert not tag.isInterest('bar')
        tag.setInterestUp(TagCount.get_by(user_id=self.data.UserData.phillipe.id, tag_id=self.data.TagData.bar.id))
        assert tag.isInterest('bar')

        # un tag que no es Interest, no pasa a serlo después de una acción de usuario
        assert not tag.isInterest('baz')
        tag.setInterestUp(TagCount.get_by(user_id=self.data.UserData.phillipe.id, tag_id=self.data.TagData.baz.id))
        assert not tag.isInterest('baz')

    def test_tagDemotion(self):
        # tag interesante, deja de serlo
        assert tag.isInterest('foo')
        tag.setInterestDown(TagCount.get_by(user_id=self.data.UserData.phillipe.id, tag_id=self.data.TagData.foo.id))
        assert not tag.isInterest('foo')

class TestItem(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.UserData, 
                popfixtures.TagData,
                popfixtures.GlobalConfigData,
                popfixtures.VideoData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)


    def test_save_description(self):
        video = Video.get_by(external_id='yt_sin_description')
        assert video.description is None
        video.description = 'Una Description'
        dbsession.flush()
        dbsession.remove()
        video = Video.get_by(external_id='yt_sin_description')
        assert video.description == 'Una Description'
