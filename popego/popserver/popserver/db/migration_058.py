# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 058
# 'avatar_mtime' (modification timestamp of users avatar) column
# for 'users' table

migration = [
    ("""
	ALTER TABLE users ADD COLUMN avatar_mtime timestamp;
     """, 
     """
	ALTER TABLE users DROP COLUMN avatar_mtime;
     """),
]

