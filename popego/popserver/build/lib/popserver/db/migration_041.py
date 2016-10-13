# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
      ALTER TABLE artists DROP CONSTRAINT artists_item_id_fkey;
      ALTER TABLE artists ADD  CONSTRAINT artists_item_id_fkey FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE bookmarks DROP CONSTRAINT bookmarks_item_id_fkey;
      ALTER TABLE bookmarks ADD  CONSTRAINT bookmarks_item_id_fkey FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE photos DROP CONSTRAINT photos_item_id_fkey;
      ALTER TABLE photos ADD  CONSTRAINT photos_item_id_fkey FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE songs DROP CONSTRAINT songs_item_id_fkey;
      ALTER TABLE songs ADD  CONSTRAINT songs_item_id_fkey FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE videos DROP CONSTRAINT videos_item_id_fkey;
      ALTER TABLE videos ADD  CONSTRAINT videos_item_id_fkey FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE tags_items DROP CONSTRAINT tags_items_inverse_fk;
      ALTER TABLE tags_items ADD  CONSTRAINT tags_items_inverse_fk FOREIGN KEY (items_id) REFERENCES items (id) ON DELETE CASCADE;

      ALTER TABLE tags_useritems DROP CONSTRAINT tags_user_items_inverse_fk;
      ALTER TABLE tags_useritems ADD  CONSTRAINT tags_user_items_inverse_fk FOREIGN KEY (user_items_id) REFERENCES user_items (id) ON DELETE CASCADE;
    """,
    """\
      SELECT 1;
    """),
]



        
