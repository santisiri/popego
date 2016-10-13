# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render
from popserver import forms

from authkit.authorize.pylons_adaptors import authorize 
from authkit.permissions import ValidAuthKitUser, And
from popserver.lib.authkitutil import UserInRoute

import popserver.lib.helpers as h
import popserver.model as model

class BaseController(WSGIController):

    # Indica si el usuario esta logueado
    _isLoggedIn = False

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        
        # load the user if exists
        self.user = None
        if 'REMOTE_USER' in environ:
            self._setUserByUsername(environ['REMOTE_USER'])
            self._setPersistentCookie(environ['REMOTE_USER'])
            self._isLoggedIn = True
        elif 'popego_user' in request.cookies:
            self._setUserByUsername(request.cookies['popego_user'])
            self._isLoggedIn = False
        
        try:
          return WSGIController.__call__(self, environ, start_response)
        finally:
          model.dbsession.remove()

    def _login(self, username):
        request.environ['paste.auth_tkt.set_user'](username)
        self._setUserByUsername(username)

    def _logout(self):
        response.delete_cookie('popego_user')
        
    def _isUserAuthenticated(self):
        #return not self.user is None
        return self._isLoggedIn

    def _getBaseUrl(self):
        return request.scheme + '://' + request.host

    def _setUserByUsername(self, username):
        self.user = model.User.get_by(username=username)
        
    def _setPersistentCookie(self, username):
        # TODO Generar una cookie "segura"
        cookieName = 'popego_user'
        if cookieName not in request.cookies or request.cookies[cookieName] != username:
          response.set_cookie(cookieName, username, expires=3600*24*365*10) 

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
