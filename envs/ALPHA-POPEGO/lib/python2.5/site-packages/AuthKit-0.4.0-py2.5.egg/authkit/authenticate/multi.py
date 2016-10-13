"""Middleware that can dynamically change the stack based on status or headers

Used in the authentication middleware to intercept 401 responses and put the 
appropriate middleware into the stack to prompt the user to sign in.
"""

from paste.auth import multi
import logging

log = logging.getLogger('authkit.authenticate.multi')

class MultiHandler(multi.MultiHandler):

    def __init__(self, application):
        multi.MultiHandler.__init__(self, application)
        self.checker = []

    def add_checker(self, name, checker):
        self.checker.append((checker,self.binding[name]))
            
    def __call__(self, environ, start_response):
        status_ = []
        headers_ = []
        exc_info_ = []
        
        def app(environ, start_response):
            def find(status, headers, exc_info=None):
                status_.append(status)
                headers_.append(headers)
                exc_info_.append(exc_info)
                log.debug("Status: %r, Headers: %r", status, headers)
            return self.default(environ, find)
        
        def logging_start_response(status, headers, exc_info=None):
            log.debug("Matched binding returns status: %r, headers: %r, "
                      "exc_info: %r", status, headers, exc_info)
            return start_response(status, headers, exc_info)
        
        def check():
            for (checker, binding) in self.predicate:
                if checker(environ):
                    log.debug(
                        "MultMiddleware self.predicate check() returning %r", 
                        binding)
                    environ['authkit.multi'] = True
                    return binding(environ, logging_start_response)
            for (checker, binding) in self.checker:
                if not len(status_):
                    raise Exception('No status was returned by the applicaiton')
                if not len(headers_):
                    raise Exception('No headers were returned by the '
                                    'application')
                if checker(environ, status_[0], headers_ and headers_[0] or []):
                    log.debug(
                        "MultiMiddleware self.checker check() returning %r", 
                        binding
                    )
                    environ['authkit.multi'] = True
                    return binding(environ, logging_start_response)
            return None
        
        app_iter = app(environ, start_response)
        if not status_:
            raise Exception('WSGI start_response was not called before a result'
                            ' was returned')
        
        result = check()
        if result is None:
            log.debug("Multi: No binding was found for the check")
            start_response(status_[0], 
                           headers_ and headers_[0] or [],
                           exc_info_[0])
            return app_iter
        
        # Close app_iter if necessary
        if hasattr(app_iter, 'close'):
            app_iter.close()
        
        return result

def status_checker(environ, status, headers):
    """
    Used by AuthKit to intercept statuses specified in the config file 
    option ``authkit.intercept``.
    """
    log.debug(
        "Status checker recieved status %r, headers %r, intecept %r", 
        status, 
        headers, 
        environ['authkit.intercept']
    )
    if str(status[:3]) in environ['authkit.intercept']:
        log.debug("Status checker returns True")
        return True
    log.debug("Status checker returns False")
    return False

class AuthSwitcher:
    def __init__(self):
        pass

    def __call__(self, environ, status, headers):
        if status_checker(environ, status, headers):
            return self.switch(environ, status, headers)
        return False

    def switch(self, environ, status, headers):
        return False

