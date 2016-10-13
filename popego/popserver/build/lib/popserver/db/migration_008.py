""" Agregar description a itemgroups """

__docformat__ = "restructuredtext"


migration = [
    ("""\
        ALTER TABLE itemgroups ADD COLUMN description character varying(512);
        """, 
     """\
        ALTER TABLE itemgroups DROP COLUMN description;
    """),
]
