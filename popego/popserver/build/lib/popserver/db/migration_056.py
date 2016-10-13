# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 056
# Widgets

migration = [
    ("""
	CREATE TABLE widgets
	(
	  id serial NOT NULL,
	  user_id int4 NOT NULL,
	  widget_template varchar(50),
	  widget_theme varchar(16),
	  best_referrer varchar(255),
	  last_seen timestamp,
	  CONSTRAINT widgets_pk PRIMARY KEY (id),
	  CONSTRAINT widgets_users_fk FOREIGN KEY (user_id)
	      REFERENCES users (id) MATCH SIMPLE
	      ON UPDATE NO ACTION ON DELETE NO ACTION
	) 
	WITHOUT OIDS;
	ALTER TABLE widgets OWNER TO popego;

     """, 
     """
	DROP TABLE widgets;
     """),
]

