from popserver.lib import model_setup
from popserver.model import * 
from popserver.sync.cache import updateAccount
from sqlalchemy import or_

#Inicializo el dbmapping
import os
import getopt, sys

def fixme():
   u = User()
   u.expunge()

def getAccountsByServices(user, services):
    if services is None:
       return user.accounts
    else:
       services = [service.lower() for service in services]
       return [account for account in user.accounts if account.service.name.lower() in services]

def importData(users, services, dryrun=False):
    # FIXME
    # Inicializa algo en elixir para que los fields sean InstrumentedAttributes
    # en vez de Fields
#    fixme()

    q = User.query
    if users is not None:
      cond = [User.username==user for user in users]
      q = q.filter(or_(*cond))

    for user in q.all():
      print 'Importando usuario %s' % user.displayname
      accounts = getAccountsByServices(user, services)
      for account in accounts:
        print '... Importando %s' % account.service.name 
        if not dryrun:
          updateAccount(account)
      


def usage():
  print sys.argv[0] + " [-d|--dry-run] (-a | [--all-users|--users=user1,user2,...]" \
                      " [--all-services|--services=service1,service2,...])"


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "adh", ["help", "all-users", "all-services", \
                                                        "users=", "services=", "dry-run"] )
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    
    if(len(opts) == 0):
      usage()
      sys.exit(2)

    users = None 
    services = None
    dryrun = False

    for o, a in opts:
        if o in ("-h", "--help"):
          usage()
          sys.exit()
        if o == "--users":
          users = a.split(",")
        if o == "--services":
          services = a.split(",")
        if o in ("-d", "--dry-run"):
          dryrun = True

    importData(users, services, dryrun)


if __name__ == "__main__":
    main()



