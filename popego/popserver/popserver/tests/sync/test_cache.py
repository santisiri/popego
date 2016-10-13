# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.model import *
from popserver.tests import *
from fixture import DataTestCase
from popserver.tests import  popfixtures
import types


# # Guardamos el getAgent original para restorearlo en el teardown
# orig_getAgent = Service.getAgent

# """ Tests para el importador """

# class TestUserDataImporter(DataTestCase, TestModel):

#     fixture = dbfixture
#     datasets = [popfixtures.UserData, popfixtures.ServiceTypeData, popfixtures.ServiceData, popfixtures.AccountData, 
#                 popfixtures.VideoData, popfixtures.UserItemData, popfixtures.ItemGroupData, popfixtures.TagData]

#     def setUp(self):
#         TestModel.setUp(self)
#         DataTestCase.setUp(self)
#         self.synchronizer = CacheSynchronizer()

#     def tearDown(self):
#         DataTestCase.tearDown(self)
#         TestModel.tearDown(self)
#         Service.getAgent = types.MethodType(orig_getAgent, None, Service)
        
#     def test_newgroup_with_newuseritems_with_newitems(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v2', 
#                                title='yt_v2_title', 
#                                description='yt_v2_description', 
#                                externalURL='yt_v2_exturl', 
#                                embedURL='yt_v1_embed')
#                     ui = UserItem(item=v1)
#                     crazy_house = ItemGroup(name='crazy_house', external_id='crazy_house', items=[ui])
                    
#                     cache_api.newGroup(crazy_house)
        
#             return YouTubeAgentStub()

#         athos = User.get_by(username='athos')
#         assert len(athos.accounts[0].item_groups) == 0
        
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(athos)
#         athos = User.get_by(username='athos')
        
#         assert len(athos.accounts[0].item_groups) == 1        
        
#         g = athos.accounts[0].item_groups[0]
#         assert g.name == 'crazy_house'
#         assert g.external_id == 'crazy_house'
#         assert len(g.items) == 1
#         assert type(g.items[0].item) == Video
#         assert g.items[0].item.external_id == 'yt_v2'
#         assert g.items[0].item.service == Service.query.get(3)
#         assert g.is_null_group == False
        
        
#     def test_phillipe(self):
#         phillipe = User.get_by(username='phillipe')
#         assert phillipe.accounts[0].username == 'futureshorts'
#         assert len(phillipe.accounts[0].item_groups) == 1
#         favorites = phillipe.accounts[0].item_groups[0] 
#         assert favorites.name == 'favorites'
#         assert len(favorites.items) == 1
#         assert favorites.items[0].item.title == 'title_yt_v1'
        
#     def test_athos_and_phillipe_have_same_video(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v1', 
#                                title='title_yt_v1', 
#                                description='video description 1', 
#                                externalURL='http://youtube.com/1/external', 
#                                embedURL='http://youtube.com/1/embed')
#                     ui = UserItem(item=v1)
#                     crazy_house = ItemGroup(name='crazy_house', external_id='crazy_house', items=[ui])
                    
#                     cache_api.newGroup(crazy_house)
        
#             return YouTubeAgentStub()
        
#         athos = User.get_by(username='athos')
#         assert len(athos.accounts[0].item_groups) == 0
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(athos)
        
#         phillipe = User.get_by(username='phillipe')
#         athos = User.get_by(username='athos')
#         philv = phillipe.accounts[0].item_groups[0].items[0].item
#         athosv = athos.accounts[0].item_groups[0].items[0].item
#         assert philv.id == athosv.id
#         assert philv is athosv
        
#     def test_phillipe_adds_same_video_to_another_group(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v1', 
#                                title='title_yt_v1', 
#                                description='video description 1', 
#                                externalURL='http://youtube.com/1/external', 
#                                embedURL='http://youtube.com/1/embed')
#                     ui = UserItem(item=v1)
#                     crazy_house = ItemGroup(name='crazy_house', external_id='crazy_house', items=[ui])
                    
#                     cache_api.newGroup(crazy_house)
        
#             return YouTubeAgentStub()
        
#         phillipe = User.get_by(username='phillipe')
#         assert len(phillipe.accounts[0].item_groups) == 1
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(phillipe)
        
#         phillipe = User.get_by(username='phillipe')
#         assert len(phillipe.accounts[0].item_groups) == 2
#         assert phillipe.accounts[0].item_groups[0].name == 'favorites'
#         assert phillipe.accounts[0].item_groups[1].name == 'crazy_house'
#         assert len(phillipe.accounts[0].item_groups[0].items) == 1
#         assert len(phillipe.accounts[0].item_groups[1].items) == 1
#         uitem1 = phillipe.accounts[0].item_groups[0].items[0]
#         uitem2 = phillipe.accounts[0].item_groups[1].items[0]
#         assert uitem1.id == uitem2.id
#         assert uitem1 is uitem2

    
#     def test_phillipe_adds_new_video_to_his_group(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v2', 
#                                title='yt_v2_title', 
#                                description='yt_v2_description', 
#                                externalURL='yt_v2_exturl', 
#                                embedURL='yt_v1_embed')
#                     ui = UserItem(item=v1)
#                     g = cache_api.getGroup('yt_gr01')

#                     cache_api.newItem(g, ui)
#             return YouTubeAgentStub()
        
#         phillipe = User.get_by(username='phillipe')
#         assert len(phillipe.accounts[0].item_groups) == 1
#         assert len(phillipe.accounts[0].item_groups[0].items) == 1
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(phillipe)
        
#         phillipe = User.get_by(username='phillipe')
#         assert len(phillipe.accounts[0].item_groups) == 1
#         assert phillipe.accounts[0].item_groups[0].name == 'favorites'
#         assert len(phillipe.accounts[0].item_groups[0].items) == 2
#         uitem1 = phillipe.accounts[0].item_groups[0].items[0]
#         uitem2 = phillipe.accounts[0].item_groups[0].items[1]
#         assert uitem1.item.external_id == 'yt_v1'
#         assert uitem2.item.external_id == 'yt_v2'

        
#     def test_pepinot_adds_existing_useritem_to_his_group(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v1', 
#                                title='yt_v1_title', 
#                                description='video description 1', 
#                                externalURL='http://youtube.com/1/external', 
#                                embedURL='http://youtube.com/1/embed')
#                     ui = UserItem(item=v1)
#                     g = cache_api.getGroup('yt_gr10')

#                     cache_api.newItem(g, ui)
#             return YouTubeAgentStub()
        
#         pepinot = User.get_by(username='pepinot')
#         assert len(pepinot.accounts[0].item_groups) == 2
#         assert len(pepinot.accounts[0].item_groups[0].items) == 1
#         assert len(pepinot.accounts[0].item_groups[1].items) == 1
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(pepinot)
        
#         pepinot = User.get_by(username='pepinot')
#         assert len(pepinot.accounts[0].item_groups) == 2
#         yt_gr10 = pepinot.accounts[0].getItemGroup('yt_gr10')
#         yt_gr11 = pepinot.accounts[0].getItemGroup('yt_gr11')
#         assert yt_gr10 is not None
#         assert yt_gr11 is not None
#         assert len(yt_gr11.items) == 1
#         assert len(yt_gr10.items) == 2
         
#         uitem1 = yt_gr11.items[0]
#         uitem2 = yt_gr10.items[1]
#         assert uitem1.item.external_id == 'yt_v1'
#         assert uitem2.item.external_id == 'yt_v1'
#         assert uitem1.item is uitem2.item
#         assert uitem1.id == uitem2.id
#         assert uitem1 is uitem2
            
#     def test_pepinot_adds_two_new_groups_with_same_useritem_with_new_item(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v2', 
#                                title='yt_v2_title', 
#                                description='video description 2', 
#                                externalURL='http://youtube.com/2/external', 
#                                embedURL='http://youtube.com/2/embed')
#                     ui = UserItem(item=v1)
#                     crazy_house = ItemGroup(name='crazy_house', external_id='crazy_house', items=[ui])
#                     pepi_group = ItemGroup(name='pepi_group', external_id='pepi_group', items=[ui])

#                     cache_api.newGroup(crazy_house)
#                     cache_api.newGroup(pepi_group)
                    
#             return YouTubeAgentStub()
        
#         pepinot = User.get_by(username='pepinot')
#         assert len(pepinot.accounts[0].item_groups) == 2
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(pepinot)
        
#         pepinot = User.get_by(username='pepinot')
#         assert len(pepinot.accounts[0].item_groups) == 4
#         crazy_house = pepinot.accounts[0].getItemGroup('crazy_house')
#         pepi_group = pepinot.accounts[0].getItemGroup('pepi_group')
#         assert crazy_house is not None
#         assert pepi_group is not None
#         assert len(crazy_house.items) == 1
#         assert len(pepi_group.items) == 1
         
#         uitem1 = crazy_house.items[0]
#         uitem2 = pepi_group.items[0]
#         assert uitem1.item.external_id == 'yt_v2'
#         assert uitem2.item.external_id == 'yt_v2'
#         assert uitem1.item is uitem2.item
#         assert uitem1 is uitem2
        
        
#     def test_pepinot_adds_to_existing_group_new_video_with_existing_tag(self):
#         def getAgentStub(self):
#             class YouTubeAgentStub(object):
#                 def updateUserGraph(self, account, cache_api):
#                     v1 = Video(external_id='yt_v2', 
#                                title='yt_v2_title', 
#                                description='video description 2', 
#                                externalURL='http://youtube.com/2/external', 
#                                embedURL='http://youtube.com/2/embed')
#                     v1.tags.append(Tag(name='foo'))
#                     ui = UserItem(item=v1)
#                     g = cache_api.getGroup('yt_gr10')
                    
#                     cache_api.newItem(g, ui)
                    
#             return YouTubeAgentStub()
        
#         pepinot = User.get_by(username='pepinot')
#         assert Tag.get_by(name='foo') is not None
#         assert len(pepinot.accounts[0].item_groups) == 2
#         Service.getAgent = types.MethodType(getAgentStub, None, Service)
#         self.synchronizer.sync(pepinot)
        
#         pepinot = User.get_by(username='pepinot')
#         v1 = Video.get_by(external_id='yt_v2')
#         v2 = Video.get_by(external_id='yt_v1')
#         tag1 = filter(lambda t: t.name == 'foo', v1.tags)[0]
#         tag2 = filter(lambda t: t.name == 'foo', v2.tags)[0]
#         assert tag1 is tag2
