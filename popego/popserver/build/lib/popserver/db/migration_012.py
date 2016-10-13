#-*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 011
# Last update - Account

migration = [
    ("""\
        ALTER TABLE accounts ALTER COLUMN user_id SET NOT NULL;
        ALTER TABLE accounts ALTER COLUMN service_id SET NOT NULL;
     """, 
     """\
        ALTER TABLE accounts ALTER COLUMN service_id DROP NOT NULL;
        ALTER TABLE accounts ALTER COLUMN user_id DROP NOT NULL;
     """),
]

