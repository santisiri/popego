import logging

from popserver.ai.interest import tag as tag_interest
from popserver.lib.base import *
from popserver.model import User, TagCount, Tag
from pylons.decorators import rest

log = logging.getLogger(__name__)

class InterestsController(BaseController):
    
    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    @rest.restrict('POST')
    def setTagInterest(self, tag):
        tc = TagCount.query.filter(TagCount.user_id == self.user.id).join('tag').filter(Tag.name == tag).first()
        if request.params['direction'] == 'down':
            tag_interest.setInterestDown(tc)
            
        return ''
        
