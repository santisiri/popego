#-*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 013
# New Entity Bookmark

migration = [
    ("""\
      ALTER TABLE users ADD COLUMN quote VARCHAR(255);
     """, 
     """\
      ALTER TABLE users DROP COLUMN quote;
     """),
]

