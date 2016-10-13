#-*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 013
# New Entity Bookmark

migration = [
    ("""\
      CREATE TABLE bookmarks (
              item_id INTEGER NOT NULL,
              url VARCHAR(2048) NOT NULL,
              PRIMARY KEY (item_id),
               FOREIGN KEY(item_id) REFERENCES items (id)
      );
     """, 
     """\
      DROP TABLE bookmarks;
     """),
]

