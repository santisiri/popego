# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.tests import *
from fixture import DataTestCase
import popserver.tests.popfixtures as fx
from popserver.model import *

class TestApplicationCache(DataTestCase, TestController):
    fixture = dbfixture
    datasets = [fx.UserData, 
                fx.ServiceTypeData,
                fx.ServiceData,
                fx.AccountData
                ]

    def setUp(self):
        TestController.setUp(self)
        DataTestCase.setUp(self)


    def tearDown(self):
        DataTestCase.tearDown(self)
        TestController.tearDown(self)

    def test_theme_modification(self):
        darty = User.get_by(username='darty')
        authEnviron = { 'REMOTE_USER':darty.username }
        themeUrl = url_for(controller='website/widgets', action='theme', \
             username=darty.username, id=1)
 
        resp = self.app.post(themeUrl, 
                             status=200,
                             params={ "theme": "aaaaaa"},
                             extra_environ=authEnviron)
        assert "ok" in resp
        darty = User.get_by(username='darty')
        assert darty.widgets[0].theme == "aaaaaa"
        

        
