# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from routes import url_for
from urllib import basejoin as urljoin
from webhelpers import *
from paste.deploy.converters import aslist

import os
import random

"""
Empaquetar en algun lado o no...depende cuan desorganizado este...
"""

# ATTENZIONE - ACHTUNG
# config/environment.py asigna el atributo config a este modulo:
# popserver.lib.helpers.config = config


from random import randint, choice
def gimme_first_valid(arr, nonvalid=['']):
    for x in arr:
        if x is not None and x not in nonvalid:
            return x
    return ''
    
def gimme_anyone(arr):
    return choice(arr)

def gimme_value_level(value, max=100, range=["very high", "high", "regular", "low", "very low"]):
    step = float(max + 1) / len(range)
    return range[ abs(int(value/step)  - (len(range) -1)) ]

def gimme_gender_pronoun(gender='M'):
    if gender=='F':
        return 'She'
    else: # default (for gender 'M' or None)
        return 'He'

import string

def asset_src(path):
    """ retorna un url absoluto hacia el recurso ubicado en ``http://popego_asset_host/path``
        donde ``popego_asset_host`` es el valor definido en popego.asset_host 
        si config['pylons.g'].revision (en los globals) no es nulo, se appendea un query string
        con ese valor.
    """
    # TODO OPTIMIZE ME
    # inicializar el arreglo de asset_hosts at module load time
    # así, es una cagada: estoy parseando popego.asset_hosts cada vez
    asset_hosts = aslist(config.get('popego.asset_hosts', None), ',', True) or ['']
    if config['pylons.g'].revision is not None:
        path += '?' + config['pylons.g'].revision
    return urljoin(string.strip(asset_hosts[path.__hash__() % len(asset_hosts)]), path)

import time, datetime

def url_for_user_avatar(user, size=100, force=False):
    # TODO: cuando force == True, habria que evitar que el request
    # del avatar se haga a los asset hosts
    if user.avatar_mtime or force:
	src = '/upload/user_avatars/%s.%s.jpg?%s' \
			% (user.username, size, int(time.mktime((user.avatar_mtime or datetime.datetime.now()).timetuple())))
    else:
	# FIXME: caso especial: para que el avatar_nopic_150.png 
	# (utilizado en widget/content) no tenga resize a 140 por CSS:
	if size == 150 and 'widget/content' in current_url():
		size = 140
	src = '/images/website/avatar_nopic_%s.png' % size
    return asset_src(src)

