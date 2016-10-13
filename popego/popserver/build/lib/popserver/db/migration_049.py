# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 048
# Countries

migration = [
    ("""\
        ALTER TABLE user_items ADD COLUMN import_date TIMESTAMP WITHOUT TIME ZONE;
        UPDATE user_items set import_date = NOW();
        ALTER TABLE user_items ALTER COLUMN import_date SET NOT NULL;

        ALTER TABLE items ADD COLUMN import_date TIMESTAMP WITHOUT TIME ZONE;
        UPDATE items set import_date = NOW();
        ALTER TABLE items ALTER COLUMN import_date SET NOT NULL;
        
        ALTER TABLE itemgroups ADD COLUMN import_date TIMESTAMP WITHOUT TIME ZONE;
        UPDATE itemgroups set import_date = NOW();
        ALTER TABLE itemgroups ALTER COLUMN import_date SET NOT NULL;
     """, 
     """\
        ALTER TABLE user_items DROP COLUMN import_date;
        ALTER TABLE items DROP COLUMN import_date;
        ALTER TABLE itemgroups DROP COLUMN import_date;
     """),
]

