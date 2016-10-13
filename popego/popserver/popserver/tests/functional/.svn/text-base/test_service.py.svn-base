from popserver.tests import *
from fixture import DataTestCase
import popserver.tests.popfixtures as fx
from popserver.model import *

class TestServiceController(DataTestCase, TestController):
    fixture = dbfixture
    datasets = [fx.UserData, 
                fx.ServiceTypeData,
                fx.ServiceData,
                fx.AccountData
                ]

    def setUp(self):
        TestController.setUp(self)
        DataTestCase.setUp(self)

        self.flickr = self.data.ServiceData.flickr
        self.darty = self.data.UserData.dartagnan
        self.porthos = self.data.UserData.porthos

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestController.tearDown(self)

    def test_index(self):
        authEnviron = {'REMOTE_USER':self.darty.username}
        url = url_for(controller='website/service',username=self.darty.username)

        resp = self.app.get(url,extra_environ=authEnviron)
        u = User.query.get(self.darty.id)
        for a1,a2 in zip(resp.c.accounts,u.accounts):
            self.assertEqual(a1.service_id,a2.service_id)

    def test_new(self):
        authEnviron = { 'REMOTE_USER':self.porthos.username }

        url = url_for(controller='website/service',action='new',
                      username=self.porthos.username,
                      id=self.flickr.id)
        
	resp = self.app.get(url, params={'username':'bla'}, 
			extra_environ=authEnviron)
        user = User.query.get(self.porthos.id)
        assert len(user.accounts) == 1
        assert user.accounts[0].service.id == self.flickr.id
        assert user.accounts[0].username == 'bla'

    def test_new_duplicateAccount(self):
        authEnviron = {'REMOTE_USER':self.darty.username}

        # precondition
        user = User.query.get(self.darty.id)
        assert len(user.accounts) == 3

        url = url_for(controller='website/service',action='new',
                      username=self.darty.username,
                      id=self.flickr.id)

	resp = self.app.get(url, params={'username':'pinchame'}, 
			extra_environ=authEnviron,expect_errors=True)
        resp.mustcontain('SERVICE_ERROR:DUPLICATED_ACCOUNT')

#     def test_new_notAuthenticated(self):
#         url = url_for(controller='website/service',action='new',
#                       username=self.porthos.username,
#                       id=self.flickr.id)
        
#         resp = self.app.get(url, expect_errors=True)
#         assert resp.status != 200

#     def test_new_notInRoutes(self):
#         authEnviron = {'REMOTE_USER':self.porthos.username}
#         url = url_for(controller='website/service',action='new',
#                       username="cualquiera",
#                       id=self.flickr.id)
        
#         resp = self.app.get(url, expect_errors=True)
#         print url
#         assert resp.status != 200

    def test_cancel(self):
        authEnviron = {'REMOTE_USER':self.darty.username}

        # precondition
        user = User.query.get(self.darty.id)
        assert len(user.accounts) == 3


        url = url_for(controller='website/service',action='cancel',
                      username=self.darty.username,
                      id=self.flickr.id)
        
        resp = self.app.get(url, extra_environ=authEnviron)
        user = User.query.get(self.darty.id)
        self.assertEqual(len(user.accounts), 2)

#     def test_cancel_notAuthenticated(self):
#         url = url_for(controller='website/service',action='cancel',
#                       username=self.porthos.username,
#                       id=self.flickr.id)
        
#         resp = self.app.get(url,expect_errors=True)
#         assert resp.status != 200

#     def test_cancel_notInRoutes(self):
#         authEnviron = {'REMOTE_USER':self.porthos.username}
#         url = url_for(controller='website/service',action='cancel',
#                       username='cualquiera',
#                       id=self.flickr.id)
        
#         resp = self.app.get(url,expect_errors=True)
#         assert resp.status != 200

    def test_cancel_notExistent(self):
        authEnviron = {'REMOTE_USER':self.porthos.username}

        # precondition
        user = User.query.get(self.porthos.id)
        assert len(user.accounts) == 0


        url = url_for(controller='website/service',action='cancel',
                      username=self.porthos.username,
                      id=self.flickr.id)
        
        resp = self.app.get(url, extra_environ=authEnviron, expect_errors=True)
        assert resp.status == 200
        #resp.mustcontain('SERVICE_ERROR:INVALID_ID')
