# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 061
# New item: Article

migration = [
    ("""
	CREATE TABLE articles (
		item_id integer NOT NULL,
		external_url varchar(2048) NOT NULL,
		publish_date timestamp NOT NULL,
		CONSTRAINT articles_pkey PRIMARY KEY (item_id),
		CONSTRAINT articles_item_id_fkey FOREIGN KEY (item_id)
		REFERENCES items (id) MATCH SIMPLE
		ON UPDATE NO ACTION ON DELETE CASCADE
	);
     """, 
     """
	DROP TABLE articles;
     """),
]

