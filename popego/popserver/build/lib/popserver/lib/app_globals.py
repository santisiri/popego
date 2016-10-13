# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""The application's Globals object"""
from pylons import config
import glob, os
from os.path import dirname, exists, join, abspath

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self._initBundles()
        self._getRevision()

    def _getRevision(self):
        """ Intenta recuperar la revision de 'popserver' a partir de un archivo 'REVISION'
            en el app root """
        rev_file = join(dirname(abspath(__file__)), '..', '..', 'REVISION')
        self.revision = open(rev_file).read().strip() if exists(rev_file) else None

    def _initBundles(self):
        self.stylesheet_bundle_path = None
        self.javascript_bundle_path = None
        root = dirname(dirname(abspath(__file__)))

        mtime_cmp = lambda fname1, fname2: cmp(os.path.getmtime(fname1), os.path.getmtime(fname2))
        
        if config.get('popego.serve_bundled_stylesheets', False):
            bundles = glob.glob(os.path.join(root, 'public/css', 'popego_style_[0-9]*.css'))
            # si llegara a haber más de un 'bundle', traer el más nuevo (ie, mayor modification time)
            self.stylesheet_bundle_path = '/css/%s' % os.path.basename(sorted(bundles, mtime_cmp)[-1]) if len(bundles) > 0 else None
        
#         if config.get('popego.serve_bundled_javascripts', False):
#             bundles = glob.glob(os.path.join(root, 'public/javascripts', 'popego_scripts_[0-9]*.css'))
#             # si llegara a haber más de un 'bundle', traer el más nuevo (ie, mayor modification time)
#             self.javascript_bundle_path = '/javascripts/%s' % os.path.basename(sorted(bundles, mtime_cmp)[-1]) if len(bundles) > 0 else None

