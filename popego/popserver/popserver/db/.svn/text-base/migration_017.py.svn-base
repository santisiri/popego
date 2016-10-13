""" Datos """

__docformat__ = "restructuredtext"

# Agrega la columna is_media en service_types
migration = [
    ("""\
        ALTER TABLE service_types ADD COLUMN is_media BOOLEAN DEFAULT TRUE;
        UPDATE service_types SET is_media = TRUE;
        ALTER TABLE service_types ALTER COLUMN is_media SET NOT NULL;
        """, 
     """\
        ALTER TABLE service_types DROP COLUMN is_media;
    """)
]
