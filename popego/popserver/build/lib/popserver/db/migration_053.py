# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 052
# home_url para Account

migration = [
    ("""
        ALTER TABLE accounts ADD COLUMN home_url VARCHAR(1024);
     """, 
     """
        ALTER TABLE accounts DROP COLUMN home_url;
     """),
]

