# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import urllib2
from itertools import imap, takewhile
import re, md5
from popserver.lib.functional import memo
from popserver.lib.util import strToDatetime

PAGE_SIZE = 100
POPULARITY_RG = re.compile('saved by ([0-9]*) ')
PAGES_RG = re.compile('page [0-9]* of ([0-9]*)')
JSON_RG = re.compile('Delicious\.posts = \[.+\]')

def accountHome(account):
    return "http://del.icio.us/%s" % account.username


def userExists(username):
    # bajar la data JSON
    # si la lista de links no es vacia (Delicious.posts == []), asumimos que el usuario existe
    try:
        fp = urllib2.urlopen('http://del.icio.us/feeds/json/%s' % username)
        json_feed = fp.read()
    except urllib2.HTTPError:
        return False

    return re.search(JSON_RG, json_feed) is not None


def updateAccount(account, cacheApi):
    if account.home_url is None:
        account.home_url = accountHome(account)

    if account.last_updated is None:
        # create Default Group
        cacheApi.addGroup(None,name='Delicious',is_null_group=True)
        generator = iBookmarkEntries(account.username)
        _parseEntries(cacheApi, generator)
    else:
        generator = iBookmarkEntries(account.username)
        actualItemsIds = cacheApi.groupItems(None)
        isUnknown = lambda e: _getId(e) not in actualItemsIds
        generator = takewhile(isUnknown, generator)
        _parseEntries(cacheApi, generator)

    _getId.clear()

def _parseEntries(cacheApi, generator):
    for e in generator:
        extId = _getId(e)
        cacheApi.addItem(extId, itemAttrs(e))
        cacheApi.bindItem2Group(None, extId)

def iBookmarkEntries(username):
    page = fetchPage(username,1)
    mainDiv = page.find('div',id='main')
    
    pagesText = mainDiv.find('p','pager').next.nextSibling
    
    match = PAGES_RG.search(pagesText)
    if match is None:
        totalPages = 1
    else:
        totalPages = int(match.group(1))
                      
    for li in mainDiv.find('ol','posts').findAll('li','post'):
        yield li
        
    for n in range(2,totalPages+1):
        page = fetchPage(username,n)
        mainDiv = page.find('div',id='main')
        
        for li in mainDiv.find('ol','posts').findAll('li','post'):
            yield li
            
def fetchPage(username,page):
    url = 'http://del.icio.us/%s?setcount=%d&page=%d' %\
        (username,PAGE_SIZE,page)
    return BeautifulSoup(urlopen(url).read())

@memo(1)
def _getId(entry):
    itemAnchor = entry.find('a','pop')
    if itemAnchor is not None:
        id = itemAnchor.get('href')[5:]
    else:
        url = entry.h4.a.get('href')
        id = md5.new(url).hexdigest()
    return id

def itemAttrs(entry):
    attrs = dict()

    attrs['title'] = entry.h4.a.string
    attrs['url']   = entry.h4.a.get('href')
                      
    dateStr = entry.find('span','date').get('title')
    attrs['creation_date'] = strToDatetime(dateStr)

    itemAnchor = entry.find('a','pop')
    if itemAnchor is not None:
        id = itemAnchor.get('href')[5:]
        attrs['popularity'] = int(POPULARITY_RG.search(itemAnchor.string).group(1))
        attrs['serviceUrl'] = 'http://del.icio.us/url/%s' % id
    else:
        external_id = md5.new(attrs['url']).hexdigest()
        attrs['popularity'] = 1
        attrs['serviceUrl'] = 'http://del.icio.us/url/%s' % external_id
    
    attrs['user_tags'] = [anchor.string.strip() for anchor in entry.findAll('a','tag')]

    return attrs
