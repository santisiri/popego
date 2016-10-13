# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""Setup the popserver application"""
import logging

from paste.deploy import appconfig
from pylons import config

from popserver.config.environment import load_environment
import elixir

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup popserver here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    
