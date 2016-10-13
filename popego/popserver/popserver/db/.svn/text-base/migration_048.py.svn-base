# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 048
# Countries

migration = [
    ("""\
        CREATE TABLE compatibility (
           user1_id INTEGER NOT NULL,
           user2_id INTEGER NOT NULL,
           compatibility INTEGER,
           PRIMARY KEY (user1_id, user2_id),
           CONSTRAINT compatibility_user1_id_fk FOREIGN KEY(user1_id) 
             REFERENCES users (id) ON DELETE cascade,
           CONSTRAINT compatibility_user2_id_fk FOREIGN KEY(user2_id) 
             REFERENCES users (id) ON DELETE cascade
        );

        CREATE INDEX ix_compatibility_user1_id ON compatibility (user1_id);
        CREATE INDEX ix_compatibility_user2_id ON compatibility (user2_id);

     """, 
     """\
	DROP TABLE compatibility;
     """),
]

