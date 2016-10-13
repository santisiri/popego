# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 050
# Tabla de Feedback

migration = [
    ("""\
        CREATE TABLE feedback
        (
          id serial NOT NULL,
          user_id integer NOT NULL,
          type varchar(20) NOT NULL,
          comment text NOT NULL, 
          creation_date timestamp without time zone DEFAULT now() NOT NULL
        );
        ALTER TABLE ONLY feedback ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);
        ALTER TABLE ONLY feedback ADD CONSTRAINT feedback_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id);
        
  """, 
     """\
        DROP TABLE feedback;
     """),
]

