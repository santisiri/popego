# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import feedparser
from time import mktime
from datetime import datetime
from popserver.lib.functional import compose

BASE_URL = 'http://twitter.com/statuses/user_timeline/'


def accountHome(account):
	return "http://twitter.com/%s" % account.username

def userExists(username):
	try:
		_getFeed(_getFeedUrl(username))
	except:
		return False

	return True

def updateAccount(account, cacheApi):
	# create default group if it does not exist
	if account.last_updated is None:
		cacheApi.addGroup(None, name='Twitter', is_null_group=True)
	# remember account home
	if account.home_url is None:
		account.home_url = accountHome(account)
	# construct feed and parse each entry
	feed = _getFeed(_getFeedUrl(account.username))
	for entry in feed.entries:
		if not _parseEntry(entry, cacheApi):
			break


# Private functions

def _getFeed(feedUrl):
	feed = feedparser.parse(feedUrl)
	if feed.bozo != 0:
		raise feed.bozo_exception
	return feed

def _getFeedUrl(username):
	return BASE_URL + username + '.rss'

def _parseEntry(entry, cacheApi):
	# stop parsing entries if quote has no id or it already exists
	ext_id = entry.get('id')
	if ext_id is None or cacheApi.itemExists(ext_id):
		return False
	# convert entry to quote dict and add to cache if valid
	quote = _entryToQuote(entry)
	if quote:
		cacheApi.addItem(ext_id, quote)
		cacheApi.bindItem2Group(None, ext_id)
	return True

def _entryToQuote(entry):
	# Validation of required attributes
	title = entry.get('title', '')
	published = entry.get('published_parsed') \
		or entry.get('updated_parsed')
	if not title or not published:
		return None
	# Feed entry to quote (dictionary) conversion
	quote = dict()
	quote['title'] = _removeUsernameAtStart(title)
	quote['description'] = _removeUsernameAtStart(entry.get('summary', ''))
	quote['external_url'] = entry.get('link', '')
	quote['creation_date'] = datetime.utcfromtimestamp(mktime(published))
	return quote

def _removeUsernameAtStart(quote):
	i = quote.find(': ')
	return quote[i + 2:] if i >= 0 else quote

