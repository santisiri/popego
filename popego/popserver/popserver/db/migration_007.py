""" Agregar external_url a Photos """

__docformat__ = "restructuredtext"


migration = [
    ("""\
        ALTER TABLE photos ADD COLUMN external_url VARCHAR(512);
        """, 
     """\
        ALTER TABLE photos DROP COLUMN external_url;
    """),
]
