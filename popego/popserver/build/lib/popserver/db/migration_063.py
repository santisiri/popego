# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 063
# Cache-friendly

migration = [
    ("""
	ALTER TABLE users DROP COLUMN theme;
    ALTER TABLE widgets RENAME widget_template TO template;
    ALTER TABLE widgets RENAME widget_theme TO theme;
    ALTER TABLE widgets DROP CONSTRAINT widgets_pk;
    ALTER TABLE widgets DROP CONSTRAINT widgets_users_fk;
    ALTER TABLE widgets ALTER COLUMN id TYPE INTEGER;
    UPDATE widgets SET id = 1;
    ALTER TABLE widgets ADD CONSTRAINT widgets_pk PRIMARY KEY (id, user_id);
    ALTER TABLE widgets ADD CONSTRAINT widgets_user_fk FOREIGN KEY(user_id) 
                                        REFERENCES users (id) ON DELETE cascade;
    ALTER TABLE widgets ALTER COLUMN id DROP DEFAULT;
       
     """, 
     """
    CREATE TABLE widgets_tmp
    (
        id serial NOT NULL,
        user_id int4 NOT NULL,
        widget_template varchar(50),
        widget_theme varchar(16),
        best_referrer varchar(255),
        last_seen timestamp
    );

    INSERT INTO widgets_tmp (user_id, widget_template, widget_theme, best_referrer, last_seen)
     SELECT user_id, template, theme, best_referrer, last_seen FROM widgets;

    DROP TABLE widgets;
    ALTER TABLE widgets_tmp RENAME TO widgets;
    
    ALTER TABLE widgets ADD CONSTRAINT widgets_pk PRIMARY KEY (id);
    ALTER TABLE widgets ADD CONSTRAINT widgets_users_fk FOREIGN KEY (user_id)
        REFERENCES users (id) MATCH SIMPLE
            ON UPDATE NO ACTION ON DELETE NO ACTION;

	ALTER TABLE users ADD COLUMN theme VARCHAR(32); 
     """),
]

