# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 062
# New item: Quote 

migration = [
    ("""
	ALTER TABLE users DROP COLUMN quote;
	CREATE TABLE quotes (
		item_id integer NOT NULL,
		external_url varchar(1024) NOT NULL,
		CONSTRAINT quotes_pkey PRIMARY KEY (item_id),
		CONSTRAINT quotes_item_id_fkey FOREIGN KEY (item_id)
		REFERENCES items (id) MATCH SIMPLE
		ON UPDATE NO ACTION ON DELETE CASCADE
	);
     """, 
     """
	ALTER TABLE users ADD COLUMN quote VARCHAR(255);
	DROP TABLE quotes;
     """),
]

