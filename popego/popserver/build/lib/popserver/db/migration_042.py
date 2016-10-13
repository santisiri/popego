#-*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 042
# Textos (prompt, etc) de Servicios

migration = [
    ("""\
         ALTER TABLE services ADD COLUMN prompt_text VARCHAR(40) DEFAULT 'username:';
         ALTER TABLE services ADD COLUMN added_text VARCHAR(40) DEFAULT 'added user';
         UPDATE services SET prompt_text = 'username or video URL:' WHERE name = 'YouTube';
         UPDATE services SET prompt_text = 'twitter.com/' WHERE name = 'Twitter';
      """,
    """\
         ALTER TABLE services DROP COLUMN prompt_text;
         ALTER TABLE services DROP COLUMN added_text;
    """),
]
