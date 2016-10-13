__docformat__ = "restructuredtext"

migration = [
    ("""\
         ALTER TABLE services ADD COLUMN item_factory character varying(255);
      
      """,
    """\
         ALTER TABLE services DROP COLUMN item_factory;
    """),
]
