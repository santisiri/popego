# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 059
# CacheResource

migration = [
    ("""
        CREATE TABLE cache_resource (
          type VARCHAR(100) NOT NULL,
          id VARCHAR(100) NOT NULL,
          tag VARCHAR(100),
          last_modified TIMESTAMP WITHOUT TIME ZONE,
          PRIMARY KEY (type, id)
        )
     """, 
     """
        DROP TABLE cache_resource;
     """),
]
