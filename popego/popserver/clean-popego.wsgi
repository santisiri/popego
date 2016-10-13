# WSGI HANDLER FOR POPEGO HOSTED ON http://clean-popego
APP_PATH = '/home/popego/clean-popego/trunk/popserver'
import site
site.addsitedir('/usr/local/pythonenv/CLEAN-POPEGO/lib/python2.5/site-packages')
import os, sys
sys.path.append(APP_PATH)
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/apache2/python-egg-cache'
from paste.deploy import loadapp
application = loadapp('config:%s/clean-popego.ini' % APP_PATH)
