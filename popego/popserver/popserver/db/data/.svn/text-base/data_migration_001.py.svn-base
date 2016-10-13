""" Crear tabla de revision """

__docformat__ = "restructuredtext"

migration = [
    ("""\
        CREATE TABLE data_revision (
            data_revision_id INT NOT NULL
        )""", 
     """\
        DROP TABLE IF EXISTS data_revision"""),

    # Subsequent migrations don't need to manage this value.  The
    # migrate.py script will take care of it.

    ("""\
        INSERT INTO data_revision (data_revision_id) VALUES (1)""",
     """\
        DELETE FROM data_revision""")
]
