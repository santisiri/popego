"""Create the revision table with a revision_id column."""

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
        CREATE TABLE revision (
            revision_id INT NOT NULL
        )""", 
     """\
        DROP TABLE IF EXISTS revision"""),

    # Subsequent migrations don't need to manage this value.  The
    # migrate.py script will take care of it.

    ("""\
        INSERT INTO revision (revision_id) VALUES (1)""",
     """\
        DELETE FROM revision""")
]
