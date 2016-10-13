# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 023
# Dropear NOT null de songs.photo_url

migration = [
    ("""
        ALTER TABLE songs ALTER COLUMN photo_url DROP NOT NULL;
     """, 
     """
        ALTER TABLE songs ALTER COLUMN photo_url SET NOT NULL;
     """),
]

