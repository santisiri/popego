import logging

from popserver.lib.base import *
from routes import url_for

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        if self._isUserAuthenticated():
            return redirect_to(url_for(controller='website/users', 
                                       action='home',
                                       username=self.user.username))
        else: 
            return render('/website/home/index.mako')
