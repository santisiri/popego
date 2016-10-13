""" """

__docformat__ = "restructuredtext"

migration = [
    ("""\
         ALTER TABLE songs DROP COLUMN name;
         ALTER TABLE songs DROP COLUMN photo_url;
         ALTER TABLE artists DROP COLUMN name;
      """,
    """\
         ALTER TABLE songs ADD COLUMN name varchar(512) NOT NULL;
         ALTER TABLE songs ADD COLUMN photo_url varchar(512) NOT NULL;
         ALTER TABLE artists ADD COLUMN name varchar(512) NOT NULL;
    """),
]
