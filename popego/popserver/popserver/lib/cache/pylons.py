from __future__ import absolute_import

from email.Utils import parsedate, parsedate_tz, formatdate
from pylons import request, response
from pylons import config
from pylons.util import class_name_from_module_name
from zope.interface import implements

from datetime import datetime
import time
from . import api
from .config import CodePoint
import md5

import logging

log = logging.getLogger('popserver_cache')


class PylonsTagManager(object):
    implements(api.ITagManager)

    def __init__(self):
        self.default_tag = self.newTag()

    def extractTag(self, call):
        ims = parsedate(request.headers.get('If-Modified-Since', None))
        return (request.headers.get('If-None-Match',None), 
                datetime(ims[0], ims[1], ims[2], ims[3], ims[4], ims[5]) if ims is not None else None)

    def injectTag(self, tag, retValue):
        delHeaders(response, ['Pragma'])
        response.headers['Cache-Control'] = 'max-age=0,must-revalidate'
        response.headers['ETag'] = tag[0]
        response.headers['Last-Modified'] = formatdate(time.mktime(tag[1].utctimetuple()) - time.timezone, False, True)
        log.info('TIME TAG: %s' % tag[1])
        log.info('INJECT TAG. Last-Modified: %s' % response.headers['Last-Modified'])
        return retValue

    def newTag(self):
        now = datetime.utcnow()
        d = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        return (md5.md5(str(d)).hexdigest(), d)

    def defaultTag(self):
        return self.default_tag

def delHeaders(response, keys):
    for key in keys:
        for dictKey in response.headers.keys():
            if key.lower() == dictKey.lower():
                del(response.headers[dictKey])
                break

class PylonsHitResponseGenerator(object):
    implements(api.IHitResponseGenerator)

    def responseFor(self, call):
        delHeaders(response, ['Pragma', 'Cache-Control', 'Content-Type'])

        response.status_code = 304
        return ""

class PylonsActionMethodResolver(object):
    implements(api.IActionMethodResolver)

    def __init__(self):
        self.basePackage = config['pylons.package'] + '.controllers.'

    def get(self, controller=None, action=None, condition=None):
        klass = self._find_controller(controller)
        return CodePoint(getattr(klass, action), condition)

    def _find_controller(self, controller):
        full_module_name = self.basePackage + controller.replace('/', '.')
        module = __import__(full_module_name, fromlist='__name__')
        module_name = controller.split('/')[-1]
        class_name = class_name_from_module_name(module_name) + 'Controller'

        controller = getattr(module, class_name)
        return controller

def controller_action(controller_name, action_name, condition=None):
    pamr = PylonsActionMethodResolver()
    return pamr.get(controller_name, action_name, condition)
    

# fetchers
def idOnEnviron(key):
    def returnIn(call):
        return request.environ.get(key, None)

    return returnIn

# TODO Llevar esto a un modulo propio de popego.
# el resto es propio de pylons only

from popserver.model import CacheResource, GlobalConfig

class PopegoDBCachePersistence(object):
    implements(api.ICachePersistence)

    def invalidate(self, resource, newTag):
        type, id = resource
        cr = CacheResource.get_by(type=type,id=id)
        if cr is None:
            cr = CacheResource(type=type,id=id)
        cr.tag = newTag[0]
        cr.last_modified = newTag[1]
        cr.flush()
        log.info("persister#invalidate - cd.last_modified: %s" % cr.last_modified)

    def getLastValue(self, resources):
        isNotNone = lambda cr: cr is not None
        tuple2CacheResource = lambda r: CacheResource.get_by(type=r[0],id=r[1])
        crs = filter(isNotNone, map(tuple2CacheResource, resources))

        if len(crs) > 0:
            lastCr = crs[0]
            for cr in crs[1:]:
                if cr.last_modified > lastCr.last_modified:
                    lastCr = cr
            log.info("persister#getLastValue - lastCr.last_modified.timetuple: %s" % lastCr.last_modified.utctimetuple())
            return (lastCr.tag, lastCr.last_modified)

        return None



