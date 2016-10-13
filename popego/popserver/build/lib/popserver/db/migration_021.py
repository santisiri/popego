""" Datos """

__docformat__ = "restructuredtext"

# UserItem refiere a User

migration = [
    ("""\
         ALTER TABLE user_items ADD COLUMN user_id INTEGER;
         UPDATE user_items SET user_id = (
           SELECT DISTINCT(accounts.user_id)
           FROM accounts, itemgroups, itemgroups_items
           WHERE accounts.id = itemgroups.account_id
            AND itemgroups.id = itemgroups_items.itemgroups_id
            AND itemgroups_items.user_items_id = user_items.id
         ); 
         ALTER TABLE user_items ADD CONSTRAINT user_items_user_id_fk FOREIGN KEY(user_id) REFERENCES users (id) 
            ON DELETE cascade;
         ALTER TABLE user_items ALTER COLUMN user_id SET NOT NULL;
          
      """,
    """\
         ALTER TABLE user_items DROP CONSTRAINT user_items_user_id_fk; 
         ALTER TABLE user_items DROP COLUMN user_id;
    """),
]
