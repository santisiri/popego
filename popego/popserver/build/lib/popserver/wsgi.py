# popserver.wsgi
# modulo expone un atributo 'application' (WSGIApplication) para facilitar el deployment
# la variable de entorno POPEGO_CONF debe contener el path al archivo de configuracion de la aplicacion
import os, sys
from paste.deploy import loadapp
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
application = loadapp('config:%s/%s' % (os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.path.basename(os.environ['POPEGO_CONF'])))
