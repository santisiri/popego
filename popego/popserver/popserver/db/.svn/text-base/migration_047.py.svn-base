# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 047
# Countries

migration = [
    ("""\
	CREATE TABLE countries
	(
	  id varchar(2) NOT NULL,
	  name varchar(64),
	  CONSTRAINT countries_pk PRIMARY KEY (id)
	) 
	WITHOUT OIDS;
	ALTER TABLE countries OWNER TO popego;
	ALTER TABLE users RENAME country TO country_id;
	ALTER TABLE users ADD CONSTRAINT users_country_id_fk FOREIGN KEY (country_id) REFERENCES countries (id) ON UPDATE RESTRICT ON DELETE RESTRICT;
     """, 
     """\
	ALTER TABLE users DROP CONSTRAINT users_country_id_fk;
	ALTER TABLE users RENAME country_id TO country;
	DROP TABLE countries;
     """),
]

