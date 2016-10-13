# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 050
# Tabla de Feedback: user_id puede ser NULL cuando el usuario es anonimo

migration = [
    ("""\
	ALTER TABLE feedback ALTER COLUMN user_id DROP NOT NULL;
  """, 
     """\
	ALTER TABLE feedback ALTER COLUMN user_id SET NOT NULL;
     """),
]

