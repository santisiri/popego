""" Faltaba NOT NULL en account_id de itemgroups"""

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
        ALTER TABLE itemgroups ALTER COLUMN account_id SET NOT NULL;
        """, 
     """\
        ALTER TABLE itemgroups ALTER COLUMN account_id DROP NOT NULL;
    """),
]
