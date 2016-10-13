# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
__all__ = ['Compatibility']

import elixir
from sqlalchemy import types

class Compatibility(elixir.Entity):
    compatibility = elixir.Field(types.Integer)
    user1 = elixir.ManyToOne('popserver.model.users.User', 
                             colname='user1_id', ondelete='cascade',
                             primary_key=True)
    user2 = elixir.ManyToOne('popserver.model.users.User',
                             colname='user2_id', ondelete='cascade',
                             primary_key=True)
    elixir.using_options(tablename='compatibility')
