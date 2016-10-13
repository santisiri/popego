# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.model import *
from popserver.tests import *
from fixture import DataTestCase
from popserver.tests import popfixtures
from popserver.agents.flickr_client.FlickrClient import FlickrClient
from popserver.agents.flickr_client import xmltramp
import types
import urllib


# guardamos el getattr original para restorearlo en el teardown
orig_getAttr = FlickrClient.__getattr__

class TestFlickrAgent(TestModel, DataTestCase):
    fixture = dbfixture
    datasets = [popfixtures.UserData, popfixtures.ServiceTypeData, popfixtures.ServiceData, popfixtures.AccountData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)
        self.user = self.data.UserData.dartagnan
        self.flickr_svc = self.data.ServiceData.flickr
        self.account = Account.get_by(user_id=self.user.id, service_id=self.flickr_svc.id)
       
        FlickrClient.__getattr__ = types.MethodType(mock_flickrclient_getattr, None, FlickrClient)

        self.agent = self.flickr_svc.getAgent()

    def tearDown(self):
        dbsession.clear()
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)
        FlickrClient.__getattr__ = orig_getAttr

    def test_getItems(self):
        self.agent.flickrUserID = '15234225@N00'
        items = self.agent.getItems(page=1, per_page=50)
        assert len(items) == 2
        assert items[0]['external_id'] == '2075891275'
        assert items[1]['external_id'] == '1460569161'

#     def test_getUserGraph(self):
#         graph = self.agent.getUserGraph(self.account)
#         assert len(graph) == 14

#         barcamp_group = filter(lambda g: str(g.external_id) == '72157602203941886', graph)[0]
#         assert barcamp_group.name == 'Barcamp BA 2007'
#         assert len(barcamp_group.items) == 1
#         assert barcamp_group.items[0].item.external_id == '1460569161' # foto en photoset barcamp
        
#         null_group = graph[-1]
#         assert len(null_group.items) == 1
#         assert null_group.items[0].item.external_id == '2075891275'
        
def mock_flickrclient_getattr(self, method):
    url_file_map = {
        'flickr_people_findByUsername-username=jazzido' : 'people_findByUsername',
        'flickr_people_getPublicPhotos-per_page=50&user_id=15234225%40N00&page=1' : 'people_getPublicPhotos-1',
        'flickr_people_getPublicPhotos-per_page=50&user_id=15234225%40N00&page=2' : 'people_getPublicPhotos-2',
        'flickr_people_getPublicPhotos-per_page=200&user_id=15234225%40N00&page=1' : 'people_getPublicPhotos-1',
        'flickr_people_getPublicPhotos-per_page=200&user_id=15234225%40N00&page=2' : 'people_getPublicPhotos-2',
        'flickr_photos_getInfo-photo_id=2075891275' : 'photos_getInfo-2075891275',
        'flickr_photos_getInfo-photo_id=1460569161' : 'photos_getInfo-1460569161',
        'flickr_photosets_getList-user_id=15234225%40N00' : 'photosets_getList',
        'flickr_photos_getAllContexts-photo_id=2075891275' : 'photos_getAllContexts-2075891275',
        'flickr_photos_getAllContexts-photo_id=1460569161' : 'photos_getAllContexts-1460569161',
        'flickr_photosets_getInfo-photoset_id=72157602203941886' : 'photosets_getInfo'
    }
    def method(_self=self, _method=method, **params):
        import popserver.tests as t
        samplesPath = t.__path__[0] + '/samples/flickr'
        url = 'file://%s/%s' % (samplesPath, url_file_map[_method + '-' + urllib.urlencode(params)])
        try:
            rsp = xmltramp.load(url)
        except:
            return None
        
        return _self._parseResponse(rsp)

    return method
