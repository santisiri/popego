__docformat__ = "restructuredtext"

migration = [
    ("""\
         INSERT INTO globalconfig VALUES('interest.tagInterestThreshold', '10');
         INSERT INTO globalconfig VALUES('interest.tagInterestAddFactor', '2');
      """,
    """\
         DELETE FROM globalconfig where property = 'interest.tagInterestThreshold';
         DELETE FROM globalconfig where property = 'interest.tagInterestAddFactor';
    """),
]
