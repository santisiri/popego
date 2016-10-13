# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from gdata.service import GDataService
from popserver.lib.util import strToDatetime
import urllib2
from functools import partial
from itertools import takewhile
from popserver.lib.functional import memo

# TODO: description para Group


# GData API
cli = GDataService(server='gdata.youtube.com')

TAG_SCHEME = 'http://gdata.youtube.com/schemas/2007/keywords.cat'

def accountHome(account):
    return "http://www.youtube.com/user/%s" % account.username


def userExists(username):
    try:
        urllib2.urlopen('http://gdata.youtube.com/feeds/users/%s' % username)
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
        actualItemsIds = cacheApi.groupItems(gExtId)
        for it in actualItemsIds:
            cacheApi.removeItemFromGroup(gExtId, it)
        _parseItems(gExtId, cacheApi, generator)

    getId.clear()

def getDefaultGroups(username):
    return [(feedUrl(username,'favorites'),'Favorites'),
            (feedUrl(username,'uploads')  ,'Uploads'  )]
    


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
        changedGroups.extend([extId for extId, name in 
                              getDefaultGroups(username)])        

        for e in iPlaylistEntries(username):
            if lastUpdate < strToDatetime(e.published.text):
                newGroups.append(entry2group(e))
            elif lastUpdate < strToDatetime(e.updated.text):
                changedGroups.append(entry2group(e)[0])
    else:
        newGroups = getDefaultGroups(username) 
        newGroups.extend(entry2group(e) for e in iPlaylistEntries(username))

    return newGroups,changedGroups

def iPlaylistEntries(username):
    plFeed = cli.GetFeed(feedUrl(username,'playlists'))
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
        if isValidEntry(e): 
            yield e
    newIndex = 1 + len(feed.entry)

    while newIndex < total:
        feed = cli.GetFeed(baseUrl + "?start-index=" + str(newIndex))
        for e in feed.entry: 
            if isValidEntry(e): 
                yield e
        newIndex += len(feed.entry)


def feedUrl(username, feed):
    return 'http://gdata.youtube.com/feeds/users/%s/%s' % (username, feed)
        

def entry2group(entry):
    name = entry.title.text
    external_id = entry.FindExtensions('feedLink')[0].attributes['href']
    return (external_id, name)

def isValidEntry(entry):
    group = entry.FindExtensions('group')[0]
    isFlash = lambda c: (c.attributes['type'] == \
                             'application/x-shockwave-flash')
    flvContent = filter(isFlash, group.FindChildren('content'))
    return len(flvContent) == 1

@memo(1)
def getId(entry):
    group = entry.FindExtensions('group')[0]
    return group.FindChildren('player')[0].attributes['url']


def itemAttrs(entry):
    attrs = dict()

    if entry.published is not None:
        attrs['creation_date'] = strToDatetime(entry.published.text)
    else:
        attrs['creation_date'] = strToDatetime(entry.updated.text)
        
    group = entry.FindExtensions('group')[0]
    attrs['title'] = group.FindChildren('title')[0].text
    attrs['description'] = group.FindChildren('description')[0].text
    attrs['author'] = entry.author[0].name.text
    attrs['externalURL'] = \
        group.FindChildren('player')[0].attributes['url']
    
    isFlash = lambda c: (c.attributes['type'] == \
                             'application/x-shockwave-flash')
    flvContent = filter(isFlash, group.FindChildren('content'))
    assert len(flvContent) == 1
    attrs['embedURL'] = flvContent[0].attributes['url'] 
    
    # thumbnails
    thumbs = filter(lambda t: int(t.attributes['width']) == 130,
                    group.FindChildren('thumbnail'))
    attrs['thumbnails'] = []
    for th in thumbs:
        vth = dict()
        vth['width']  = int(th.attributes['width'])
        vth['height'] = int(th.attributes['height'])
        vth['time'] = th.attributes['time']
        vth['url'] = th.attributes['url']
        attrs['thumbnails'].append(vth)

    attrs['item_tags'] = [c.term for c in entry.category 
                  if c.scheme == TAG_SCHEME]

    return attrs
