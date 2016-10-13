""" Datos """

__docformat__ = "restructuredtext"

# Un UserItem no puede tener duplicado el user y el item

migration = [
    ("""\
         ALTER TABLE user_items ADD CONSTRAINT user_item_unique UNIQUE(user_id, item_id);
          
      """,
    """\
         ALTER TABLE user_items DROP CONSTRAINT user_item_unique;
    """),
]
