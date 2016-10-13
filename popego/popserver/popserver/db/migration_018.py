""" Datos """

__docformat__ = "restructuredtext"

# Agrega la columna is_media en service_types
# Inserta 'quotes' en service_types y 'Twitter' en Service
migration = [
    ("""\
        ALTER TABLE bookmarks ADD COLUMN serviceUrl varchar(2048);
        ALTER TABLE bookmarks ALTER COLUMN serviceUrl SET STORAGE EXTENDED; 
        ALTER TABLE bookmarks ALTER COLUMN serviceUrl SET NOT NULL;
        """, 
     """\
        ALTER TABLE bookmarks DROP COLUMN serviceUrl;
    """),
    ("""\
        ALTER TABLE bookmarks ADD COLUMN popularity int4;
        ALTER TABLE bookmarks ALTER COLUMN popularity SET NOT NULL;
     """,
     """\
        ALTER TABLE bookmarks DROP COLUMN popularity;
    """)
]
