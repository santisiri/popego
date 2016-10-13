# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.tests import *
from popserver.model import User
from fixture import DataTestCase
import popserver.tests.popfixtures as fx

class TestInterestsController(DataTestCase, TestController):

    fixture = dbfixture
    datasets = [fx.UserData, 
                fx.TagData,
                fx.GlobalConfigData]


    def setUp(self):
        TestController.setUp(self)
        DataTestCase.setUp(self)
        self._authEnviron = { 'REMOTE_USER': self.data.UserData.dartagnan }

        # a darty y phillipe les interesa 'foo'
        tag.setInterestUp(TagCount.get_by(user=self.data.UserData.dartagnan, tag=self.data.TagData.foo))
        tag.setInterestUp(TagCount.get_by(user=self.data.UserData.phillipe, tag=self.data.TagData.foo))
        # a aramis tambien le interesa 'bar'
        tag.setInterestUp(TagCount.get_by(user=self.data.UserData.aramis, tag=self.data.TagData.bar))

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)
        self._authEnviron = None
