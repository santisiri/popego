# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 056
# 'user_agent' column for 'feedback' table

migration = [
    ("""
	ALTER TABLE feedback ADD COLUMN user_agent varchar(255)
     """, 
     """
	ALTER TABLE feedback DROP COLUMN user_agent;
     """),
]

