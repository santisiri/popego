# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 016
# Agregar asociacion tags<->items

migration = [
    ("""
        CREATE TABLE tags_items
        (
          tags_id integer NOT NULL,
          items_id integer NOT NULL,
          CONSTRAINT tags_items_pkey PRIMARY KEY (tags_id, items_id),
          CONSTRAINT tags_items_fk FOREIGN KEY (tags_id)
            REFERENCES tags (id) MATCH SIMPLE
            ON UPDATE NO ACTION ON DELETE NO ACTION,
          CONSTRAINT tags_items_inverse_fk FOREIGN KEY (items_id)
            REFERENCES items (id) MATCH SIMPLE
            ON UPDATE NO ACTION ON DELETE NO ACTION
        );
     """, 
     """
        DROP TABLE tags_items;
     """),
]

