#-*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 043
# Settings: Personal info

migration = [
    ("""\
      ALTER TABLE users ADD COLUMN website VARCHAR(64);
      ALTER TABLE users ADD COLUMN gender VARCHAR(1);
      ALTER TABLE users ADD COLUMN birthdate TIMESTAMP;
      ALTER TABLE users ADD COLUMN country VARCHAR(2);
     """, 
     """\
      ALTER TABLE users DROP COLUMN website;
      ALTER TABLE users DROP COLUMN gender;
      ALTER TABLE users DROP COLUMN birthdate;
      ALTER TABLE users DROP COLUMN country;
     """),
]

