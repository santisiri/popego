# FlickrClient
# Copyright (c) 2004 Michele Campeotto

import xmltramp
import sys

from urllib import urlencode


HOST = 'http://flickr.com'
PATH = '/services/rest/'
API_KEY = '3688e2ed7d18224b4d2c877c5541f89d'


class FlickrError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def __str__(self):
        return 'Flickr Error %s: %s' % (self.code, self.message)


class FlickrClient:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def __getattr__(self, method):
        def method(_self=self, _method=method, **params):
            _method = _method.replace("_", ".")
            url = HOST + PATH + "?method=%s&%s&api_key=%s" % \
                    (_method, urlencode(params), self.api_key)
            try:
                    rsp = xmltramp.load(url)
            except:
                    return None
            return _self._parseResponse(rsp)
        return method

    def _parseResponse(self, rsp):
        if rsp('stat') == 'fail':
            raise FlickrError(rsp.err('code'), rsp.err('msg'))
        
        try:
                return rsp
        except:
                return None


user = None
photoSets = None
if __name__ == '__main__':
    USER_ID = '51035543396@N01'
    
    client = FlickrClient(API_KEY)
    
    person = client.flickr_people_getInfo(user_id=USER_ID)
    photoSets = client.flickr_photosets_getList(user_id=USER_ID)
    
    print person.username, "has", len(photoSets), "photosets:",
    print ', '.join([str(set.title) for set in photoSets])
