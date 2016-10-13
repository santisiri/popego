# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.tests import *

from popserver.model import User
from formencode.api import set_stdtranslation
import paste.fixture

class TestUsersController(TestController):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.mail = 'mcortesi@gmail.com'
        self.values = dict(
            displayname='Mariano Cortesi',
            email=self.mail,
            username='mariano',
            password='pwd',
            password_confirm='pwd')

        # force language (en) for tests where validation message 
        # might be translated with gettext; see: http://formencode.org/
        # Validator.html#localization-of-error-messages-i18n    
        set_stdtranslation(domain="FormEncode", languages=["en"])

        # check no user in db
        assert User.query.filter_by(email=self.mail).count() == 0
        self.response = self.app.get(url_for(controller='website/users'))

    def tearDown(self):
        self.app.get(url_for(controller='auth',action='signout'))
        super(self.__class__, self).tearDown()

    def test_register(self):
        self._registerUser()
        assert User.query.filter_by(email=self.mail).count() == 1
     
    def _registerUser(self):
        self.fillForm(self.response.forms['profile'], self.values)
        return self.response.forms['profile'].submit()

    def test_registerUppercaseUsername(self):
        self.values['username'] = 'MariAno'
        self._registerUser()
        assert User.query.filter_by(email=self.mail).count() == 1


    def test_registerSameUsernameWithDifferentCase(self):
        self._registerUser()
        self.values['username'] = 'MarIano'
        self.values['email'] = 'another@email.com'

        self.app = paste.fixture.TestApp(self.wsgiapp)
        self.app.extra_environ['REMOTE_ADDR'] = '127.0.0.1' # Hack needed for testing things like AuthKit

        self.response = self.app.get(url_for(controller='website/users'))
        self.response = self._registerUser()
        assert User.query.filter_by(username='mariano').count() == 1
        assert 'username already exists' in self.response

    def test_register_InvalidEmail(self):
        self.mail = 'invalidEmail'
        self.values['email'] = self.mail

        self.fillForm(self.response.forms['profile'], self.values)
        r2 = self.response.forms['profile'].submit()
        assert User.query.filter_by(email=self.mail).count() == 0
        assert 'An email address must contain a single @' in r2

    def test_register_NoUsername(self):
        del self.values['username']
        self.fillForm(self.response.forms['profile'], self.values)
        r2 = self.response.forms['profile'].submit()

        assert 'class="error"' in r2
        assert User.query.filter_by(email=self.mail).count() == 0

    def test_register_InvalidUsername(self):
        self.values['username']= 'Mariano?'
        self.fillForm(self.response.forms['profile'], self.values)
        r2 = self.response.forms['profile'].submit()

        assert User.query.filter_by(email=self.mail).count() == 0
        assert 'class="error"' in r2

    def fillForm(self,form,values):
        for name,value in values.items():
            form[name]=value
