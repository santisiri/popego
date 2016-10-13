# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 015
# Agregar tabla tags y join table para useritems

migration = [
    ("""
        CREATE TABLE tags (
          id SERIAL NOT NULL, 
          name VARCHAR(256) NOT NULL, 
          PRIMARY KEY (id), 
          UNIQUE (name)
        );

        CREATE TABLE tags_useritems
        (
          tags_id integer NOT NULL,
          user_items_id integer NOT NULL,
          CONSTRAINT tags_useritems_pkey PRIMARY KEY (tags_id, user_items_id),
          CONSTRAINT tags_user_items_fk FOREIGN KEY (tags_id)
            REFERENCES tags (id) MATCH SIMPLE
            ON UPDATE NO ACTION ON DELETE NO ACTION,
          CONSTRAINT tags_user_items_inverse_fk FOREIGN KEY (user_items_id)
            REFERENCES user_items (id) MATCH SIMPLE
            ON UPDATE NO ACTION ON DELETE NO ACTION
        );
     """, 
     """
        DROP TABLE tags_useritems;
        DROP TABLE tags;
     """),
]

