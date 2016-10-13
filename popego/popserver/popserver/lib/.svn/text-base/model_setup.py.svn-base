import os
import elixir
from paste.deploy import appconfig


if 'POPEGO_CONF' in os.environ:
    confDir, confFile = os.path.split(os.environ['POPEGO_CONF'])
else:
    dn = os.path.dirname
    confDir = dn(dn(dn(os.path.abspath(__file__))))
    confFile = 'development.ini'

config = appconfig('config:' + confFile, relative_to=confDir)
elixir.metadata.bind = config['sqlalchemy.url']

