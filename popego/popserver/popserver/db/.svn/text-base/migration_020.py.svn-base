""" Datos """

__docformat__ = "restructuredtext"

# Agrega la columna is_media en service_types
# Inserta 'quotes' en service_types y 'Twitter' en Service
migration = [
    ("""\
         ALTER TABLE bookmarks RENAME COLUMN serviceurl TO "serviceUrl";
      """,
    """\
         ALTER TABLE bookmarks RENAME COLUMN "serviceUrl" TO serviceurl;
    """),
]
