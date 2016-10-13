# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
      CREATE TABLE globalconfig (
        property VARCHAR(255) PRIMARY KEY NOT NULL,
        value VARCHAR(255) NOT NULL
      );
    """,
    """\
      DROP TABLE globalconfig;
    """),
]

        
