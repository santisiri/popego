""" Faltaba NOT NULL en account_id de itemgroups"""

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
        ALTER TABLE items ADD CONSTRAINT items_external_id_service_id_key UNIQUE (external_id, service_id);
        """, 
     """\
        ALTER TABLE items DROP CONSTRAINT items_external_id_service_id_key;
    """),
]
