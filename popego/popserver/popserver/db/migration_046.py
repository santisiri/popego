# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 046
# agregar columna interest_factor a tagcounts

migration = [
    ("""
        ALTER TABLE tagcounts ADD COLUMN interest_factor INT4 NOT NULL DEFAULT 0;
     """, 
     """
        ALTER TABLE tagcounts DROP COLUMN interest_factor;
     """),
]

