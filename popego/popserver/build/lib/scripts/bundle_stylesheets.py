import os
import sys
import re
import fileinput
import pylons
from paste.deploy import loadapp
from paste.deploy.converters import asbool, aslist
from popserver.lib import helpers

if len(sys.argv) != 2:
    print "Usage: %s [path_to_ini_file]" % sys.argv[0]
    exit(1)

loadapp('config:%s' % sys.argv[1], relative_to = os.getcwd())

#helpers.config = pylons.config

make_bundle = asbool(pylons.config.get('popego.serve_bundled_stylesheets', False))
bundle_files = aslist(pylons.config.get('popego.stylesheet_bundle_files', None), ',', True)

if make_bundle is None:
    sys.stderr.write('``popego.serve_bundled_styesheets`` not defined or False. Exiting.')
    exit(1)

if len(bundle_files) == 0:
    sys.stderr.write('``popego.stylesheet_bundle_files`` not defined or empty. Exiting.')
    exit(1)

url_rex = re.compile(r'url\((.*)\)')
relative_url_rex = re.compile(r'^(?:\.\./)*(.+)$')

def fix_url(match):
    return 'url(%s)' % helpers.asset_src(relative_url_rex.sub(r'\1', match.group(1)))

for line in fileinput.input(map(lambda f: os.path.join(pylons.config['pylons.paths']['static_files'], f), bundle_files)):
    print url_rex.sub(fix_url, line)
    
