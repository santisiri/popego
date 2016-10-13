# WSGI HANDLER FOR POPEGO HOSTED ON http://alpha.popego.com
APP_PATH = '/home/popego/alpha.popego.com/current'
import site
site.addsitedir('/home/popego/alpha-popego/envs/ALPHA-POPEGO/lib/python2.5/site-packages')
import os, sys
sys.path.append(APP_PATH)
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/alpha-popego/egg-cache'
from paste.deploy import loadapp
application = loadapp('config:%s/alpha-popego.ini' % APP_PATH)
