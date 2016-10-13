# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from urllib import quote

def getUrl(environ):
    url = environ['wsgi.url_scheme']+'://'

    if environ.get('HTTP_HOST'):
        url += environ['HTTP_HOST']
    else:
        url += environ['SERVER_NAME']

        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
               url += ':' + environ['SERVER_PORT']
        else:
            if environ['SERVER_PORT'] != '80':
               url += ':' + environ['SERVER_PORT']

    url += quote(environ.get('SCRIPT_NAME',''))
    url += quote(environ.get('PATH_INFO',''))
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']

    return url


class HeaderCacheMiddleware(object):

    def __init__(self, application, headerGenerator):
        self.application = application
        self.headerGenerator = headerGenerator

    def __call__(self, environ, start_response):

        def start_cache(status,response_headers, exc_info=None):
            if status[:3] == "200" and environ.get('REQUEST_METHOD') == 'GET':
                new_headers = []
                for header in self.headerGenerator.getHeaders(getUrl(environ)):
                    if not self.isHeaderPresent(header[0], response_headers):
                        new_headers.append(header)

                response_headers.extend(new_headers)

            return start_response(status,response_headers)

        return self.application(environ,start_cache)

    def isHeaderPresent(self, header_name, headers):
        # TODO Lowercase
        return len(filter(lambda h: h[0] == header_name, headers)) > 0


import re

headerRules = [ \
    (re.compile(".*/fernando/home.*"),[("X-Pepe", "hola")]), \
    (re.compile(".*/fer/home.*"),[("X-Pepe", "hola2"), ("X-lala", "hola 3")]) \
]

class HeaderGenerator(object):

    def __init__(self, headerRules=[]):
        self.headerRules = headerRules
    
    def getHeaders(self, url):
        for rule in self.headerRules:
            if rule[0].match(url) is not None:
                return rule[1]

        return [] 
