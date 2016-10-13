# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from gdata.service import GDataService
from popserver.lib.util import strToDatetime
import urllib2
from functools import partial
from itertools import takewhile
from popserver.lib.functional import memo, findFirst

# TODO: description para Group


# GData API
cli = GDataService(server='picasaweb.google.com')

TAG_SCHEME = 'http://gdata.youtube.com/schemas/2007/keywords.cat'

def accountHome(account):
    return "http://picasaweb.google.com/%s" % account.username


def userExists(username):
    try:
        urllib2.urlopen('http://picasaweb.google.com/data/feed/api/user/%s' % username)
    except urllib2.HTTPError:
        return False
    return True

def updateAccount(account, cacheApi):
    """
    Given an account, it detects all new items and groups
    and register them to the ``cacheApi``
    """
    if account.home_url is None:
        account.home_url = accountHome(account)

    lastUpdate = account.last_updated
    newGroups, changedGroups = getGroupsToCheck(account.username, lastUpdate)

    for gExtId, name in newGroups:
        cacheApi.addGroup(gExtId, name=name)
        generator = iGroupEntries(gExtId)
        _parseItems(gExtId, cacheApi, generator)
    
    for gExtId in changedGroups:
        generator = iGroupEntries(gExtId)
        cacheApi.clearItemsFromGroup(gExtId)
        _parseItems(gExtId, cacheApi, generator)


    getId.clear()

def _parseItems(gExtId, cacheApi, generator):
    for entry in generator:
        extId = getId(entry)
        if not cacheApi.itemExists(extId):
            cacheApi.addItem(extId, itemAttrs(entry))
        cacheApi.bindItem2Group(gExtId, extId)

def getGroupsToCheck(username, lastUpdate):
    """
    Given the lastUpdate date, it returns a tuple
    with the new groups and the changed groups for the username
    """
    newGroups = []
    changedGroups = []

    if lastUpdate is not None:
        # we don't know if default groups have updates, 
        # so we check them
        for e in iUserGroupsEntries(username):
            if lastUpdate < strToDatetime(e.published.text):
                newGroups.append(entry2group(e))
            elif lastUpdate < strToDatetime(e.updated.text):
                changedGroups.append(entry2group(e)[0])
    else:
        newGroups = [entry2group(e) for e in iUserGroupsEntries(username)]

    return newGroups,changedGroups

def iUserGroupsEntries(username):
    plFeed = cli.GetFeed(feedUrl(username))
    return (entry for entry in plFeed.entry)

def iGroupEntries(gExtId):
    """ 
    Generator para todos los items de un grupo.
    Levanta paginas on demand
    """
    baseUrl = gExtId
    feed = cli.GetFeed(baseUrl)
    total = int(feed.total_results.text)

    for e in feed.entry: 
        yield e
    newIndex = 1 + len(feed.entry)

    while newIndex < total:
        feed = cli.GetFeed(baseUrl + "?start-index=" + str(newIndex))
        for e in feed.entry: 
            yield e
        newIndex += len(feed.entry)


def feedUrl(username, albumId=None):
    url = 'http://picasaweb.google.com/data/feed/api/user/%s' % username
    if albumId:
        url += '/albumid/%s' % albumId
    return url
        

def entry2group(entry):
    name = entry.title.text
    external_id = entry.GetFeedLink().href
    return (external_id, name)

@memo(1)
def getId(entry):
    return entry.GetHtmlLink().href


def itemAttrs(entry):
    attrs = dict()

    if entry.published is not None:
        attrs['creation_date'] = strToDatetime(entry.published.text)
    else:
        attrs['creation_date'] = strToDatetime(entry.updated.text)
        
    group = entry.FindExtensions('group')[0]

    attrs['title'] = entry.title.text
    attrs['description'] = entry.summary.text
    attrs['author'] = group.FindChildren('credit')[0].text
    attrs['external_url'] = getId(entry)
    attrs['url'] = group.FindChildren('content')[0].attributes['url'] + '?imgmax=512'
    
    # Get thumbnail of 108x144
    attrs['thumbnail_url'] = findFirst(lambda t: t.attributes['height'] == '144'
                                       or t.attributes['width'] == '144', 
                                       group.FindChildren('thumbnail')).attributes['url']

    keywords = group.FindChildren('keywords')[0].text
    attrs['user_tags'] = keywords.split(' ') if keywords else []

    return attrs
