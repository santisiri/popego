__docformat__ = "restructuredtext"

migration = [
    ("""\
         INSERT INTO globalconfig VALUES('interest.nroOfCompatibilityRanges', '10');
      """,
    """\
         DELETE FROM globalconfig where property = 'interest.nroOfCompatibilityRanges';
    """),
]
