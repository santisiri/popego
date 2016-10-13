from popserver.lib.base import *
import logging
log = logging.getLogger(__name__)

class SocialfeedController(BaseController):

    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    def index(self):
        c.user = self.user
        return render('/website/user/socialfeed.mako')

