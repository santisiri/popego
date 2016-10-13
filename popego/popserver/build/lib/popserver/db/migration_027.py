""" """

__docformat__ = "restructuredtext"

# Se agrega tabla tagcounts para sumarizar los tags de un usuario

migration = [
    ("""\
       CREATE TABLE tagcounts (
          user_id INTEGER NOT NULL,
          tag_id INTEGER NOT NULL,
          count INTEGER NOT NULL,
          PRIMARY KEY (user_id, tag_id),
          CONSTRAINT tagcounts_user_id_fk FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE cascade,
          CONSTRAINT tagcounts_tag_id_fk FOREIGN KEY(tag_id) REFERENCES tags (id) ON DELETE restrict
        );
      """,
    """\
         DROP TABLE tagcounts;
    """),
]
