# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 021
# Crear tablas para artists y songs

migration = [
    ("""

        CREATE TABLE artists (
          item_id INTEGER NOT NULL, 
          name VARCHAR(255) NOT NULL, 
          photo_url VARCHAR(512) NOT NULL, 
          PRIMARY KEY (item_id), 
          FOREIGN KEY(item_id) REFERENCES items (id)
        );

        CREATE TABLE songs (
          item_id INTEGER NOT NULL, 
          name VARCHAR(512) NOT NULL, 
          photo_url VARCHAR(512) NOT NULL, 
          artist_item_id INTEGER NOT NULL, 
          PRIMARY KEY (item_id), 
          FOREIGN KEY(item_id) REFERENCES items (id), 
          CONSTRAINT songs_artist_item_id_fk FOREIGN KEY(artist_item_id) REFERENCES artists (item_id) ON DELETE restrict
        );

        CREATE INDEX ix_songs_artist_item_id ON songs (artist_item_id)

     """, 
     """
        DROP TABLE songs;
        DROP TABLE artists;
     """),
]

