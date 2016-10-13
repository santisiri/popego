__docformat__ = "restructuredtext"

migration = [
    ("""\
         ALTER TABLE user_items ADD COLUMN row_type VARCHAR(40);
         ALTER TABLE user_items ADD COLUMN play_count INTEGER;
      """,
    """\
         ALTER TABLE user_items DROP COLUMN row_type;
         ALTER TABLE user_items DROP COLUMN play_count;
    """),
]
