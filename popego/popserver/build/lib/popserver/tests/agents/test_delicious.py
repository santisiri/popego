# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.tests.nodb_model import *
from popserver.tests import *
from popserver.tests import mock
import popserver.agents.delicious_agent as dl
from BeautifulSoup import BeautifulSoup
import itertools
from datetime import datetime
from unittest import TestCase

class Stubber(object):
   def __init__(self, module, fnName):
      self.module = module
      self.fnName = fnName

   def do(self, fnStub):
      self.cache = getattr(self.module, self.fnName)
      setattr(self.module, self.fnName, fnStub)
   def undo(self):
      setattr(self.module, self.fnName, self.cache)

def getSample(name):
   import popserver.tests as t
   f = open(t.__path__[0] + '/samples/delicious/' + name)
   return f

class TestDeliciousAgent(TestCase):
   expectations =  []

   def setUp(self):
      super(self.__class__,self).setUp()
      self.stubber = Stubber(dl,'urlopen',)
      self.account = Account(username='conito')
      self.stubber.do(self._createUrlopenMock())

   def tearDown(self):
      self._verifyUrlopenMock()
      self.stubber.undo()
      del(self.account)
      super(self.__class__, self).tearDown()

   def test_fetchPage(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1', 'conitoX10')
         ]

      page = dl.fetchPage('conito',1)
      assert page is not None

   def test_itemAttrs(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ]

      firstEntry = dl.iBookmarkEntries('conito').next()

      attrs = dl.itemAttrs(firstEntry)

      assert attrs['url'] == "http://wine-review.blogspot.com/2007/10/" \
          + "itunes-73-on-linux-with-wine.html"
      assert attrs['serviceUrl'] == "http://del.icio.us/url/" + \
          "27c86026483d844764d74857ffaf4695"
      assert attrs['title'] == 'Wine Review: iTunes 7.3 on Linux with Wine'
      self.assertEqual(attrs['user_tags'], 
                       ['itunes','wine','linux','howto'])
      assert attrs['popularity'] == 63

   def test_getId(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ]

      firstEntry = dl.iBookmarkEntries('conito').next()
      assert dl._getId(firstEntry) == '27c86026483d844764d74857ffaf4695'

    
   def test_iBookmarkEntries_firstPageOnly(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ]

      bkmGenerator = dl.iBookmarkEntries('conito')
      list(itertools.islice(bkmGenerator,0,9))
       
   def test_iBookmarkEntries_allPages(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ('http://del.icio.us/conito?setcount=100&page=2','conitoX10-page2')
         ]
      
      list(dl.iBookmarkEntries('conito'))
       
   def test_updateAccount_NewAccount(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ('http://del.icio.us/conito?setcount=100&page=2','conitoX10-page2')
         ]

      cacheApi = mock.Mock()
      cacheApi.expects(mock.once()).addGroup(
         mock.eq(None), name=mock.eq('Delicious'),is_null_group=mock.eq(True))
      cacheApi.expects(mock.exactly(20)).method('addItem')
      cacheApi.expects(mock.exactly(20)).method('bindItem2Group')

      groups = dl.updateAccount(self.account, cacheApi)
      cacheApi.verify()
                      

   def test_updateAccount_OldAccount(self):
      self.expectations = [
         ('http://del.icio.us/conito?setcount=100&page=1','conitoX10'),
         ]

      cacheApi = mock.Mock()
      cacheApi.expects(mock.once()).groupItems(mock.eq(None)).will(
         mock.return_value(['d2b95de9147b861039f85db169e28322']))
      cacheApi.expects(mock.exactly(6)).method('addItem')
      cacheApi.expects(mock.exactly(6)).method('bindItem2Group')

      self.account.last_updated = datetime(2007,5,1)
      dl.updateAccount(self.account, cacheApi)
      
      cacheApi.verify()

   def _createUrlopenMock(self):
      def urlopen(url):
         if len(self.expectations) > 0:
            exUrl, sample = self.expectations.pop(0)
            self.assertEqual(url, exUrl)
            return getSample(sample)
         else:
            assert False, "more calls than expected"
      return urlopen

   def _verifyUrlopenMock(self):
      self.assertEqual(len(self.expectations) , 0)


