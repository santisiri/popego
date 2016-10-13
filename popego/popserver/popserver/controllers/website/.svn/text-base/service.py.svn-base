import logging

from popserver.ai.interest import tag as tagInterest
from popserver.lib.base import *
from popserver.lib import jq_client
from popserver.model import User, Account, Service, ServiceType, TagCount
from sqlalchemy.orm import eagerload
import os, shutil, math
import Image

log = logging.getLogger(__name__)



class ServiceController(BaseController):

    def __init__(self, *args, **kwargs):
        super(ServiceController, *args, **kwargs)
        self.queueHostname = config.get('jqueue.hostname', 'localhost')
        self.queuePort = int(config.get('jqueue.port', 8787))

    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    def index(self):
        c.user = self.user

        c.accounts = self.user.accounts
        c.services = Service.query.all()
        c.serviceTypes = ServiceType.query.all()
    
        c.myTopTags = self._toptags(40, self.user.id)
        c.baseUrl = self._getBaseUrl()

        return render('/website/user/services.mako')

    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    @jsonify
    def new(self, username, id):
        u = self.user
        s = Service.query.get(id)
        username = request.params['username']
        count = Account.query.filter_by(user_id=u.id,service_id=s.id).count()
        
        if not s.userExists(username):
            r = {"status" : "error", \
                 "statusText" : "SERVICE_ERROR:USER_NOT_FOUND", \
                 "description" : "Yikes...user not found."}
        elif count > 0:
            r = {"status" : "error", \
                 "statusText" : "SERVICE_ERROR:DUPLICATED_ACCOUNT", \
                 "description" : "An account is already there."}
        else:    
            acc = Account(user=u,service=s,username=username)
            acc.flush()
            
            jq_client.newJob("newAccount", acc.id, 
                             self.queueHostname, 
                             self.queuePort)

            r = {"status" : "ok", \
                 "statusText" : "SERVICE:ACCOUNT_CREATED", \
                 "description" : "An account has been created."}
            
        return r
    
    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    @jsonify
    def cancel(self, username, id):   
        u = self.user
        account = Account.query.filter_by(user_id=u.id, service_id=id).first()
        if account is None: 
            r = {"status" : "error", \
                 "statusText" : "SERVICE_ERROR:INVALID_ID", \
                 "description" : "Invalid Service ID." }
        else:
            account.delete()
            account.flush()    
            r = {"status" : "ok", \
                 "statusText" : "SERVICE:ACCOUNT_REMOVE", \
                 "description" : "The account has been removed."}
       
        return r

    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    @jsonify
    def toptags(self, username):
    	# n is the number of top tags requested
    	try:
    		n = int(request.params['n'])
    		n = min(n, 100) # 100 at most
    	except Exception:
    		n = 10
	    
        return self._toptags(n, self.user.id)

    def _toptags(self, qty, user_id):
        tagCounts = tagInterest.getUserTopInterests(user_id, qty)
        r = []
        if qty > 0:
            qty = len(tagCounts)
            styles = ['lowest', 'low', 'middle', 'top','highest']
            styleSize = int(math.ceil(qty/float(len(styles))))

            tagCounts.reverse()
            for i in range(0,len(styles)):
                for t in tagCounts[i*styleSize:(i+1)*styleSize]:
                    record = dict(tagName=t.tag.name, 
                                  className= styles[i],
                                  count=t.count)
                    r.append(record)
                
            r = sorted(r, lambda x, y: cmp(x['tagName'], y['tagName']))

        return r

