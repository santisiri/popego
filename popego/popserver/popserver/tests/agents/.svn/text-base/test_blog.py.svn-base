# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import os
from popserver.model import *
from popserver.tests import *
from datetime import datetime
import popserver.tests.mock as p
from popserver.agents import blog_agent
from HTMLParser import HTMLParseError


class TestBlogAgent(TestModel):

	def setUp(self):
		super(self.__class__, self).setUp()
		# initialize here ...
		import popserver.tests as t
		self.originalpath = os.getcwd()
		self.samplepath = '%s/samples/blog' % t.__path__[0]
		fn = blog_agent._getFeed
		blog_agent._urlWrapper = self._urlWrapper

	def tearDown(self):
		os.chdir(self.originalpath)
		# ... finalize here
		super(self.__class__, self).tearDown()

	def test_accountHome(self):
		u = '%s' % datetime.now()
		a = Account(username = u)
		home = blog_agent.accountHome(a)
		self.assertEqual(home, u)

	def test_userExists(self):
		fs = ['gamesareart.html', 'la_ultima_curda.html', \
				'rss10.html', 'gamesareart.rss', \
				'la_ultima_curda.xml', 'rss10.rdf']
		usernames = [self._getFeedFilename(i) for i in fs]
		for i in usernames:
			self.assertEqual(blog_agent.userExists(i), True)

	def test_userExists_expectingFalse(self):
		u = self._getFeedFilename('nofeedlink.html')
		self.assertEqual(blog_agent.userExists(u), False)

	def test_updateAccount(self):
		u = self._getFeedFilename('la_ultima_curda.xml')
		a = Account(username = u, last_updated = None)
		a.home_url = 'http://juan.zauber.com.ar'
		cacheApiMock = p.Mock()
		cacheApiMock.expects(p.once()).addGroup(p.eq(None), \
				name=p.eq('Blog'), is_null_group=p.eq(True))
		cacheApiMock.expects(p.exactly(15)).method('itemExists') \
				.will(p.return_value(True))
		blog_agent.updateAccount(a, cacheApiMock)
		cacheApiMock.verify()

	def test_updateAccount_withExistentDefaultGroup(self):
		u = self._getFeedFilename('la_ultima_curda.xml')
		a = Account(username = u, last_updated = datetime.now())
		a.home_url = 'http://juan.zauber.com.ar'
		cacheApiMock = p.Mock()
		cacheApiMock.expects(p.exactly(15)).method('itemExists') \
				.will(p.return_value(True))
		blog_agent.updateAccount(a, cacheApiMock)
		cacheApiMock.verify()

	def test_parseEntry(self):
		entry = {'id': u'tag:juan.zauber.com.ar,2008-02-15:198',
			'published_parsed': (2008, 2, 15, 1, 48, 0, 4, 46, 0),
			'title': u'Mock title for unit test',
            'link': u'http://bala.bala.com'}
		ext_id = entry['id']
		cacheApiMock = p.Mock()
		cacheApiMock.expects(p.once()).itemExists(p.eq(ext_id)) \
				.will(p.return_value(False))
		cacheApiMock.expects(p.once()).method('addItem')
		cacheApiMock.expects(p.once()).method('bindItem2Group')
		article = blog_agent._parseEntry(entry, cacheApiMock)
		cacheApiMock.verify()
		# non-happy paths are validated in other tests

	def test_entryToArticle(self):
		tags = [{'label': None, 'scheme': None, 'term': u'art'}, \
			{'label': None, 'scheme': None, 'term': u'games'}, \
			{'label': None, 'scheme': None}]
		entry = {'author': u'juan',
			'id': u'tag:juan.zauber.com.ar,2008-02-15:198',
			'link': u'http://juan.zauber.com.ar/',
			'published': u'2008-02-15T01:48:00Z',
			'published_parsed': (2008, 2, 15, 1, 48, 0, 4, 46, 0),
			'tags': tags,
			'title': u'Mock title for unit test',
			'summary': u'This is a mock summary.',
			'updated': u'2008-02-15T01:53:06Z',
			'updated_parsed': (2008, 2, 15, 1, 53, 6, 4, 46, 0)}
		article = blog_agent._entryToArticle(entry)
		self.assertEqual(article['title'], entry['title'])
		self.assertEqual(article['description'], entry['summary'])
		self.assertEqual(article['external_url'], entry['link'])
		self.assertEqual(article['creation_date'], \
			datetime(2008, 2, 15, 4, 48, 0))
		self.assertEqual(article['item_tags'], ['art', 'games'])

	def test_entryToArticle_withNoTitle(self):
		entry = {}
		article = blog_agent._entryToArticle(entry)
		self.assertEqual(article, None)

	def test_entryToArticle_withNoDate(self):
		entry = {'title': 'bla'}
		article = blog_agent._entryToArticle(entry)
		self.assertEqual(article, None)

	def test_getFeed(self):
		entriesCount = {'gamesareart.rss': 10,
				'la_ultima_curda.xml': 15,
				'rss10.rdf': 1}
		for i in entriesCount:
			f = blog_agent._getFeed(self._getFeedFilename(i))
			self.assertEqual(len(f.entries), entriesCount[i])

	# def test_getFeedUrl(self): # is trivial
		# if urllib2 can be trusted, we'd rather test FeedLinkParser

	def test_FeedLinkParser(self):
		feedLinks = {'gamesareart.html': 'gamesareart.rss',
				'la_ultima_curda.html': 'la_ultima_curda.xml',
				'rss10.html': 'rss10.rdf'}
		for i in feedLinks:
			html = open(self._getFeedFilename(i), 'r').read()
			p = blog_agent.FeedLinkParser()
			try:
				p.feed(html)
			except HTMLParseError: # e.g. malformed html
				pass
			self.assertEqual(p.getFeedLink(), feedLinks[i])

	def test_FeedLinkParser_noFeedLink(self):
		f = 'nofeedlink.html'
		html = open(self._getFeedFilename(f), 'r').read()
		p = blog_agent.FeedLinkParser()
		p.feed(html)
		try:
			p.getFeed()
			raise Exception('getFeed was expected to raise an ' \
					'Exception due to no feed link found')
		except Exception:
			pass


	# Utility methods

	def _getFeedFilename(self, filename):
		return os.path.join(self.samplepath, filename)

	def _urlWrapper(self, url): # for stub
		localUrl = ('file://%s'  if url[-5:] == '.html' else '%s') \
				% self._getFeedFilename(url)
		return localUrl

