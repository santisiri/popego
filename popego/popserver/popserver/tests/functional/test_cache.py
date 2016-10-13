# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.tests import *
from fixture import DataTestCase
import popserver.tests.popfixtures as fx
from popserver.model import *

from popserver.lib.cache import *
from popserver.lib.cache.pylons import *
from popserver.lib.cache.persistence import *

from popserver.controllers.widget.widget import WidgetController
from popserver.controllers.website.settings import SettingsController
from time import sleep


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

        self.darty = self.data.UserData.dartagnan
        self.flickr = self.data.ServiceData.flickr
        self.showUrl = url_for(controller='widget/widget', action='show', \
             username=self.darty.username, id=1)

        self._setUpCache()

    def _setUpCache(self):
        cacheConfig = CacheConfig()

        userResourceType = cacheConfig.defineResourceType('User')
        userResourceType.cacheOn(CodePoint(WidgetController.show), idOnParameter(1)) # username es el 1er parametro posicional para Widget.show
        userResourceType.invalidateOn(CodePoint(SettingsController.personal_settings), idOnEnviron('REMOTE_USER'))
        userResourceType.invalidateOn(CodePoint(SettingsController.upload), idOnParameter(1))

        self.cm = CacheManager(MemoryCachePersistence(), PylonsTagManager(), PylonsHitResponseGenerator())
        self.cm.activate(cacheConfig)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestController.tearDown(self)
        self._tearDownCache()

    def _tearDownCache(self):
        self.cm.deactivate()

    def test_cache_hit(self):
        url = self.showUrl

        resp = self.app.get(url)
        assert resp.status == 200
        etag = resp.header('ETag', None) 
        assert etag is not None
        last_mod = resp.header('Last-Modified', None)
        assert last_mod is not None

        headers = dict()
        headers['If-None-Match'] = etag
        headers['If-Modified-Since'] = last_mod
        resp = self.app.get(url, headers=headers)
        assert resp.status == 304

    def test_cache_gives_same_etag_and_modification_date(self):
        response_headers = ('Etag', 'Last-Modified')
        url = self.showUrl

        resp = self.app.get(url, status=200)
        header_values = self._extractHeaders(resp, response_headers)

        resp = self.app.get(url, status=200)
        for header in response_headers:
            newHeaderValue = resp.header(header, None)
            assert newHeaderValue is not None
            assert newHeaderValue == header_values[header]

    def _extractHeaders(self, response, headerNames):
        header_values = {}
        for header in headerNames:
            header_values[header] = response.header(header, None) 
            assert header_values[header] is not None

        return header_values
        

    def test_cache_invalidation(self):
        header_names = ('Etag', 'Last-Modified')
        authEnviron = { 'REMOTE_USER':self.darty.username }
        settingsUrl = url_for(controller='website/settings', action='personal_settings', \
             username=self.darty.username)

        resp = self.app.get(self.showUrl, status=200)
        old_header_values = self._extractHeaders(resp, header_names)
        
        # XXX Si no se agrega el sleep el test corre tan rapido que el default 
        # tag se genera en el mismo segundo que el tag de invalidación.
        # Por lo tanto al hacerse el siguiente GET el etag y modified-since coinciden
        sleep(2)

        resp = self.app.post(settingsUrl, 
                             status=200,
                             params={ "website": None, "minibio": "", "birthmonth": "", 
                                      "country": None, "birthyear": "", "birthday": "",
                                      "gender": None, "fullname": "Manolo Aristaran", "email": "maristaran@gmail.com" },
                             extra_environ=authEnviron)
        

        
        headers = dict()
        headers['If-None-Match'] = old_header_values['Etag']
        headers['If-Modified-Since'] = old_header_values['Last-Modified']
        resp = self.app.get(self.showUrl, headers=headers)
        assert resp.status == 200
        new_header_values = self._extractHeaders(resp, header_names)
        assert new_header_values['Etag'] != old_header_values['Etag']
        assert new_header_values['Last-Modified'] != old_header_values['Last-Modified']
