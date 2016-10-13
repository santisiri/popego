# procesa un stylesheet para convertir los urls relativos a absolutos,
# usando el helper asset_src
import os
import sys
import re
import fileinput
import pylons
from paste.deploy import loadapp
from popserver.lib import helpers

if len(sys.argv) != 3:
    print "Usage: %s [path_to_ini_file] [path_to_css]" % sys.argv[0]
    exit(1)

loadapp('config:%s' % sys.argv[1], relative_to = os.getcwd())

if not os.path.exists(sys.argv[2]):
    print "%s doesn't exist"
    exit(1)

url_rex = re.compile(r'url\((.*)\)')
relative_url_rex = re.compile(r'^(?:\.\./)*(.+)$')

def fix_url(match):
    return 'url(%s)' % helpers.asset_src(relative_url_rex.sub(r'\1', match.group(1)))

for line in fileinput.input([sys.argv[2]], 1):
    print url_rex.sub(fix_url, line)

