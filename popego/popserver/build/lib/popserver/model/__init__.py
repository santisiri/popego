# -*- coding: utf-8 -*-
"""
Modulo que concentra todas las entidades de Modelo del Sistema.
"""
__docformat__='restructuredtext'

import elixir
elixir.options_defaults['autosetup'] = True

from popserver.model.services import *
from popserver.model.items import *
from popserver.model.users import *
from popserver.model.config import *
from popserver.model.exceptions import *
from popserver.model.ai import *
from popserver.model.cache import *

from elixir import session as dbsession
from elixir import metadata
