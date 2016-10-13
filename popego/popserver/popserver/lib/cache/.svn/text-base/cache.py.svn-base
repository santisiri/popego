# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from itertools import imap
from popserver.lib.functional import all
from decorator import decorator
import logging
import datetime, time

import sys

log = logging.getLogger('popserver_cache')

class CacheManager(object):
    def __init__(self, persister, tagManager, responseGenerator):
        self.tagManager = tagManager
        self.persister = persister
        self.responseGenerator = responseGenerator

    def activate(self, config):
        """ 
        Activa el cache en función de un ``cacheConfig``
        """
        if hasattr(self,'config'): self.deactivate()

        self.config = config
        log.debug("Activating CacheManager")
        log.debug("invalidate actions:")
        for codePoint, resourceFetchers in config.iInvalidateActions():
            self._decorateWithInvalidate(codePoint, resourceFetchers)
            log.debug("%s, %s" % (codePoint, resourceFetchers))
            
        log.debug("cache actions")
        for codePoint, resourceFetchers in config.iCacheActions():
            self._decorateWithCached(codePoint, resourceFetchers)
            log.debug("%s, %s" % (codePoint, resourceFetchers))

    def deactivate(self):
        for codePoint, resourceFetchers in self.config.iInvalidateActions():
            self._removeDecorator(codePoint.callable)
        for codePoint, resourceFetchers in self.config.iCacheActions():
            self._removeDecorator(codePoint.callable)

        del self.config
    
    def _removeDecorator(self, oldActionMethod):
        klass = oldActionMethod.im_class
        oldFn = oldActionMethod.im_func
        name = [name for name, func in klass.__dict__.items() 
                if hasattr(func, 'decoratee') 
                if func.decoratee is oldFn][0]
        setattr(klass, name, oldFn)        
        
    def _decorateWithInvalidate(self, codePoint, resourceFetchers):
        klass = codePoint.callable.im_class
        fn = codePoint.callable.im_func
        name = [name for name, func in klass.__dict__.items() if func is fn][0]

        @decorator
        def _invalidateInvoked(fn, *args, **kwargs):
             result = fn(*args, **kwargs)
             call = Call(fn, args, kwargs, result)

             if codePoint.condition(call):
                 tag = self.tagManager.newTag()
                 log.debug("_invalidateInvoked for %s: %s" % (fn, tag))
                 for f in resourceFetchers:
                     resource = f.fetch(call)
                     self.persister.invalidate(resource, tag)

             return result
        
        dec = _invalidateInvoked(fn)
        dec.decoratee = fn

        setattr(klass, name, dec)


    def _decorateWithCached(self, codePoint, resourceFetchers):
        klass = codePoint.callable.im_class
        fn = codePoint.callable.im_func
        name = [name for name, func in klass.__dict__.items() if func is fn][0]

        @decorator
        def _cachedInvoked(fn, *args, **kwargs):
            call = Call(fn, args, kwargs)
            if codePoint.condition(call):
                tag = self.tagManager.extractTag(call)
                resources = map(lambda f: f.fetch(call), resourceFetchers)
                lastTag = self.persister.getLastValue(resources)
                lastTag = lastTag if lastTag is not None else \
                    self.tagManager.defaultTag()
                
                log.debug("_cachedInvoked for %s - received: %s last: %s" % (fn, tag, lastTag))

                before_call = time.time()
                if tag is None or lastTag != tag:
                    log.info("MISS: %s" % call_log_repr(call))
                    retValue = self.tagManager.injectTag(lastTag, fn(*args, **kwargs))
                else: 
                    log.info("HIT: %s" % call_log_repr(call))
                    retValue = self.responseGenerator.responseFor(call)
                    log.info("Time: %f" % (time.time() - before_call))
            
                return retValue
            else:
                return fn(*args, **kwargs)

        dec = _cachedInvoked(fn)
        dec.decoratee = fn

        setattr(klass, name, dec)

    def _invalidateInvoked(self, resourceFetchers, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        call = Call(fn, args, kwargs, result)
        tag = self.tagManager.newTag()
        log.debug("_invalidateInvoked for %s: %s" % (fn, tag))
        for f in resourceFetchers:
            resource = f.fetch(call)
            self.persister.invalidate(resource, tag)
        return result

            
class Call(object):
    def __init__(self, fn, args, kwargs, result=None):
        self.function = fn
        self.args = dict(enumerate(args))
        self.args.update(kwargs)
        self.result = result

    def __repr__(self):
        return "Call<function=%(function)s, args=%(args)s>" % self.__dict__

import re
def call_log_repr(call):
    call_args = call.args.copy()
    controller_name = re.match('<(.*) object', str(call_args[0])).groups()[0]
    del(call_args[0])
    return '%s#%s(%s)' % (controller_name, call.function.func_name, call_args)
    
