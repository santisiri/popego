# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from datetime import datetime
from time import mktime
from urllib2 import urlopen
from HTMLParser import HTMLParser, HTMLParseError
from popserver.lib.functional import findFirst
from popserver.lib.util import stripHTMLTags
import feedparser


def accountHome(account):
	# for "blog accounts":
	# if home_url is set: home_url == blog url, username == feed url
	# if home_url is not set: username == blog url
	return account.home_url if account.home_url is not None \
			else account.username

def userExists(username):
	try:
		_getFeed(_getFeedUrl(username))
	except:
		try:
			_getFeed(username)
		except:
			return False

	return True

def updateAccount(account, cacheApi):
	# create default group if it does not exist
	if account.last_updated is None:
		cacheApi.addGroup(None, name='Blog', is_null_group=True)
	# set home_url and remember feed detection
	if account.home_url is None:
		blogUrl = account.username
		account.username = _getFeedUrl(blogUrl)
		account.home_url = blogUrl
	# construct feed and parse each entry
	feedUrl = account.username
	feed = _getFeed(feedUrl)
	for entry in feed.entries:
		_parseEntry(entry, cacheApi)


# Private functions

def _parseEntry(entry, cacheApi):
	# cancel if article has no id or it already exists
	ext_id = entry.get('id')
	if ext_id is None or cacheApi.itemExists(ext_id):
		return False
	# convert entry to article dict and add to cache if valid
	article = _entryToArticle(entry)
	if article:
		cacheApi.addItem(ext_id, article)
		cacheApi.bindItem2Group(None, ext_id)
	return True

def _getFeed(feedUrl):
	_applyWordpressMediaTitleHack()
	feed = feedparser.parse(_urlWrapper(feedUrl))
	if feed.bozo != 0:
		raise feed.bozo_exception
	return feed

# TODO: @retry(1, x) donde x es un URLError de connection timeout
def _getFeedUrl(blogUrl):
	html = urlopen(_urlWrapper(blogUrl)).read()
	p = FeedLinkParser()
	try:
		p.feed(html)
	except HTMLParseError: # e.g. malformed html
		pass
	feedUrl = p.getFeedLink()
	if feedUrl.startswith('/'):
		feedUrl = blogUrl + feedUrl
	return feedUrl

def _urlWrapper(url):
	return url # useful for stubbing in unit tests

def _entryToArticle(entry):
	# Validation of required attributes
	title = entry.get('title', '')
	published = entry.get('published_parsed') \
			or entry.get('updated_parsed')
	link = entry.get('link', None)
	if not title or not published or not link:
		return None
	# Feed entry to article (dictionary) conversion
	article = dict()
	article['title'] = title
	
	article['description'] = _getEntryDescription(entry)
	
	article['external_url'] = link
	article['creation_date'] = datetime.utcfromtimestamp(mktime(published))
	article['item_tags'] = [t.get('term') for t in \
			entry.get('tags', {}) if 'term' in t]
	return article


def _getEntryDescription(entry):
	# si summary esta vacio:
	#  tomo el primer entry.content[j].value de entry.content tal que entry.content[j].type sea texto o html
	# si no:
	#   tomo summary
	rv = None
	if 'summary' in entry:
		rv = entry['summary']
	elif 'content' in entry and len(entry.content) > 0:
		c = findFirst(lambda c: c.get('type', None) in ('text/html', 'text/plain'), entry['content'])
		if c is not None: rv = c['value']
	return stripHTMLTags(rv).strip() if rv is not None else None

# Hack for <media:title> tags in WordPress feeds
# that make entry titles go wrong in feedparser
# http://code.google.com/p/feedparser/issues/detail?id=83

def _applyWordpressMediaTitleHack():
	f = feedparser._FeedParserMixin
	f._start_dc_title = _wordpressMediaTitleStartHack
	f._start_media_title = _wordpressMediaTitleStartHack
	f._end_dc_title = _wordpressMediaTitleEndHack
	f._end_media_title = _wordpressMediaTitleEndHack

def _wordpressMediaTitleStartHack(self, attrsD):
	if not self._getContext().has_key('title'):
		self._start_title(attrsD)

def _wordpressMediaTitleEndHack(self):
	if not self._getContext().has_key('title'):
		self._end_title()




# Utility classes

class FeedLinkParser(HTMLParser):
	""" Detects feed links in a HTML document """

	ACCEPT_TYPES = ['application/atom+xml', 'application/rss+xml', \
			'application/rdf+xml','application/x-netcdf', \
			'application/xml']

	def __init__(self):
		HTMLParser.__init__(self)
		self.feed_links = {}
	
	def getFeedLink(self):
		# prioriza links segun el orden de ACCEPT_TYPES
		for type in self.ACCEPT_TYPES:
			if type in self.feed_links:
				return self.feed_links[type]
		raise HTMLParseError('Feed not found')

	def handle_starttag(self, tag, attrs):
		if tag != 'link':
			return
		# de los 'link' tags quedarse con los que tienen atributos
		# rel="alternate" y un type reconocido
		a = dict(attrs)
		rel = a.get('rel', '')
		type = a.get('type', '')
		link = a.get('href', '')
		if link and rel == 'alternate' and type in self.ACCEPT_TYPES:
			self.feed_links.setdefault(type, link) # set only once
	
