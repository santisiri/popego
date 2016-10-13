# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from paste.deploy import appconfig
from os.path import dirname as dn
from os.path import exists, join, abspath
from paste.deploy.converters import aslist
import os, sys

def getRevision():
    rev_file = join(dn(abspath(__file__)), '..', 'REVISION')
    return open(rev_file).read().strip() if exists(rev_file) else None

def genJavascript(base_url, asset_host):
    js = """ 
       Popego.Config.baseURL = "%s";
       Popego.Config.assetsURLs = {
          "default": "%s"
       };
       Popego.Config.revision = %s;
    """ % (base_url, asset_host, getRevision() or 'null')
    return js
    

if len(sys.argv) < 2:
    print >> sys.stderr, "Usage: %s [path_to.ini]" % sys.argv[0]
    exit()

confFile = sys.argv[1]
confDir = dn(dn(os.path.abspath(__file__)))

config = appconfig('config:' + confFile, relative_to=confDir)

print genJavascript(config['popego.base_url'], aslist(config['popego.asset_hosts'], ',')[0])
