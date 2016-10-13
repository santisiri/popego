""" agregar columna para grupo distinguido en itemgroups """

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
        ALTER TABLE itemgroups ADD COLUMN is_null_group BOOLEAN NOT NULL;
        """, 
     """\
        ALTER TABLE itemgroups DROP COLUMN is_null_group;
    """),
]
