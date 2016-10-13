__docformat__ = "restructuredtext"

migration = [
    ("""\
         DELETE FROM globalconfig WHERE 
             property = 'interest.nroOfCompatibilityRanges';
         INSERT INTO globalconfig VALUES
             ('compatibility.objCountThreshold', '100');
      """,
    """\
         INSERT INTO globalconfig VALUES
             ('interest.nroOfCompatibilityRanges', '10');
         DELETE FROM globalconfig WHERE 
             property = 'compatibility.objCountThreshold';
    """),
]
