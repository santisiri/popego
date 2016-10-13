# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""Pylons environment configuration"""
import os

from pylons import config

import popserver.lib.app_globals as app_globals
import popserver.lib.helpers
from popserver.config.routing import make_map
from paste.deploy.converters import asbool
import elixir

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='popserver',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = popserver.lib.helpers

    # easter egg :)
    config['pylons.response_options']['headers']['X-Pop'] = 'Ego!'

    # hacer que config esté disponible en el scope de popserver.lib.helpers
    popserver.lib.helpers.config = config

    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)

    # Assume that templates are encoded in utf-8
    # Can override on a per-template basis using a 'magic encoding comment'
    tmpl_options['mako.input_encoding'] = 'utf-8'

    # Configures DB Engine
    elixir.metadata.bind = config['sqlalchemy.url']
    elixir.metadata.bind.echo = True if config['sqlalchemy.echo'] == 'True' \
        else None
    elixir.options_defaults['autosetup'] = True

    if asbool(config.get('popego.cache_manager.enable', False)):
        from popserver.config import cache
        cache.enable_cache()

