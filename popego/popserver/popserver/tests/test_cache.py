# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from unittest import TestCase
from popserver.lib.cache import *
from popserver.lib.cache.api import *
from popserver.lib.cache.persistence import MemoryCachePersistence
from zope.interface import implements

class ControllerStub(object):

    def __init__(self):
        self.showSettingsCount = 0

    def onSaveSettingsRaise(self, e):
        self.e = e

    def saveSettings(self,username=None):
        if hasattr(self,'e'):
            raise self.e()
        
    def showSettings(self, username):
        self.showSettingsCount +=1
        return 'stubReturnValue'


class DumbTagManager(object):
    implements(ITagManager)

    def __init__(self, default):
        self.values = []
        self.injectedTag = None
        self.default_value = default

    def extractTag(self, call):
        return self.values.pop(0)
    
    def injectTag(self, tag, retValue):
        self.injectedTag = tag
        return retValue

    def defaultTag(self):
        return self.default_value

    def newTag(self):
        return self.values.pop(0)

    def nextValue(self, value):
        self.values.append(value)


class DumbHitResponseGenerator(object):
    implements(IHitResponseGenerator)

    def __init__(self):
        self.values = []

    def responseFor(self, call):
        return self.values.pop(0)

    def nextValue(self, value):
        self.values.append(value)
        

class TestResourceCache(TestCase):

    def setUp(self):
        config = CacheConfig()
        resource = config.defineResourceType('User')
        resource.invalidateOn(CodePoint(ControllerStub.saveSettings),
                              idFetcher=idOnParameter(1))
        resource.cacheOn(CodePoint(ControllerStub.showSettings), 
                         idFetcher= idOnParameter(1))
        self.cachePersistence = MemoryCachePersistence()
        self.tagManager = DumbTagManager('default')
        self.responseGenerator = DumbHitResponseGenerator()
        self.cacheManager = \
            CacheManager(persister = self.cachePersistence,
                         tagManager =  self.tagManager,
                         responseGenerator = self.responseGenerator)
        self.cacheManager.activate(config)

    def tearDown(self):
        self.cacheManager.deactivate()
        
    def test_invalidate(self):
        self.cachePersistence.invalidate(('User', 'pepito'), 'oldValue')
        self.tagManager.nextValue('nuevoValor')
        
        ControllerStub().saveSettings(username='pepito')
        
        assert self.cachePersistence.getLastValue([('User','pepito')]) == 'nuevoValor'
        
    def test_invalidate_not_200(self):
        self.cachePersistence.invalidate(('User', 'pepito'), 'oldValue') 
        stub = ControllerStub()
        stub.onSaveSettingsRaise(Exception)

        self.assertRaises(Exception, stub.saveSettings, username='pepito')

        assert self.cachePersistence.getLastValue([('User','pepito')]) == 'oldValue'

    def test_cache_returns_304(self):
        self.cachePersistence.invalidate(('User', 'pepito'), 'oldValue')
        self.responseGenerator.nextValue('hubo un hit!!')
        self.tagManager.nextValue('oldValue')

        stub = ControllerStub()
        value = stub.showSettings(username='pepito')

        assert value == 'hubo un hit!!'
        assert stub.showSettingsCount == 0

    def test_cache_returns_304_using_default_tag(self):
        self.responseGenerator.nextValue('hubo un hit!!')
        self.tagManager.nextValue(self.tagManager.defaultTag())

        stub = ControllerStub()
        value = stub.showSettings(username='pepito')

        assert value == 'hubo un hit!!'
        assert stub.showSettingsCount == 0
        
    def test_cache_forward_request_with_tag_in_cache(self):
        self.cachePersistence.invalidate(('User', 'pepito'), 'newValue')
        self.tagManager.nextValue('oldValue')

        self._callAndCheckInjectedTag('newValue')

    def test_cache_forward_request_with_default_tag_when_no_tag_at_all(self):
        self.tagManager.nextValue(None)

        self._callAndCheckInjectedTag(self.tagManager.defaultTag())

    def _callAndCheckInjectedTag(self, tag):
        stub = ControllerStub()
        value = stub.showSettings(username='pepito')

        assert self.tagManager.injectedTag == tag
        assert stub.showSettingsCount == 1
        assert value == 'stubReturnValue'

    def test_cache_forward_request_with_default_tag_when_tag_in_req_but_not_in_cache(self):
        self.tagManager.nextValue("oldValue")

        self._callAndCheckInjectedTag(self.tagManager.defaultTag())
    
    def test_cache_forward_request_with_last_tag_when_tag_in_cache_but_not_in_req(self):
        self.cachePersistence.invalidate(('User', 'pepito'), 'newValue')
        self.tagManager.nextValue(None)

        self._callAndCheckInjectedTag('newValue')


class TestMemoryCachePersistence(TestCase):

    def setUp(self):
        self.cachePersistence = MemoryCachePersistence()    

    def test_getLastValue_with_empty_cache(self):
        assert self.cachePersistence.getLastValue([('User', 'pepito')]) is None

    def _invalidate(self):
        self.cachePersistence.invalidate(1, ("tag1", 1))
        self.cachePersistence.invalidate(2, ("tag2", 2))
        self.cachePersistence.invalidate(3, ("tag3", 3))
        self.cachePersistence.invalidate(4, ("tag4", 4))
    
    def test_getLastValue(self):
        self._invalidate()
        assert self.cachePersistence.getLastValue([1]) == ("tag1", 1)
        assert self.cachePersistence.getLastValue([1, 2, 3, 4]) == ("tag4", 4)
 
    def test_getLastValue_preconditions(self):
        self.assertRaises(Exception, self.cachePersistence.getLastValue, None)
        self.assertRaises(Exception, self.cachePersistence.getLastValue, [])

    def test_getLastValue_with_some_empty_resources(self):
        self._invalidate()
        assert self.cachePersistence.getLastValue([1, 5, 6]) == ("tag1", 1)
        assert self.cachePersistence.getLastValue([1, 5, 7, 4]) == ("tag4", 4)
        assert self.cachePersistence.getLastValue([5, 7]) is None

    
    
