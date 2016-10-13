""" """

__docformat__ = "restructuredtext"

# Un UserItem no puede tener duplicado el user y el item

migration = [
    ("""\
         ALTER TABLE artists ALTER COLUMN photo_url DROP NOT NULL;
      """,
    """\
         ALTER TABLE artists ALTER COLUMN photo_url SET NOT NULL;
    """),
]
