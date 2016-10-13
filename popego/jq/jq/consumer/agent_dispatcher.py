from popserver.lib import model_setup

from popserver.model import * 
from popserver.lib.cache.pylons import PopegoDBCachePersistence, PylonsTagManager
from utils.decorator import retry
from popserver.services.sync import updateAccount
import sys
import traceback

# turn off alchemy warnings
import warnings
warnings.filterwarnings('ignore', ".*", Warning, "sqlalchemy.engine.*",0)

# set default encoding
reload(sys)
sys.setdefaultencoding('utf8')

@retry(1)
def doUpdate(account):
    try:
        updateAccount(account)
    finally:
        dbsession.remove()


# invalid argunments length
if len(sys.argv) != 3:
    print "Finished with Error"
    print "Invalid arguments: %s" % str(sys.argv)
    sys.exit(1)

type, accountId = sys.argv[1:3]


try:
    account = Account.get(accountId)
except Exception, e:
    ex = sys.exc_info()
    print "Finished with Error"
    traceback.print_exception(ex[0],ex[1],ex[2],file=sys.stdout)    
    # invalid Id, others
    sys.exit(1)


status = "Ok"
try:
    doUpdate(account)
    for user in account.users:
        PopegoDBCachePersistence().invalidate(
            ('User', user.username), PylonsTagManager().newTag())
except Exception, e:
    ex = sys.exc_info()
    status = "Error"
    
print "JobType: '%s' Account: '%s' Service: '%s' Status: '%s'" % \
    (type, account.username, account.service.name, status)
if status == "Error":
    traceback.print_exception(ex[0],ex[1],ex[2],file=sys.stdout)
