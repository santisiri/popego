from popserver.tests import *
from popserver.tests import popfixtures
from fixture import DataTestCase

class TestWidgetController(DataTestCase, TestController):
    fixture = dbfixture
    datasets = [popfixtures.UserData]

    def setUp(self):
        TestController.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestController.tearDown(self)


    def test_iframeContent(self):
        userData =  self.data.UserData.aramis
        response = self.app.get(url_for(controller='widget/widget',
                                        username=userData.username,
                                        action='content', id=1))
        assert hasattr(response.c,'user')
        assert response.c.user.username == userData.username
        assert userData.displayname in response
