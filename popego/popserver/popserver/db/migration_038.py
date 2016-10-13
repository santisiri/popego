# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
         ALTER TABLE users ADD COLUMN "weightedObjCount" FLOAT(10);
         ALTER TABLE services ADD COLUMN weight FLOAT(10);
         ALTER TABLE tagcounts ADD COLUMN "weightedCount" FLOAT(10);
         CREATE TABLE profileconfig (
           id SERIAL NOT NULL,
           "uItemTagWeight" FLOAT(10) NOT NULL,
           "itemTagWeight" FLOAT(10) NOT NULL,
           "consumerWeight" FLOAT(10) NOT NULL,
           "producerWeight" FLOAT(10) NOT NULL,
           PRIMARY KEY (id)
         );
         UPDATE users SET "weightedObjCount" = 1.0;
         UPDATE services SET weight = 1.0;
         UPDATE tagcounts SET "weightedCount" = count;
         ALTER TABLE users ALTER COLUMN "weightedObjCount" SET NOT NULL;
         ALTER TABLE services ALTER COLUMN weight SET NOT NULL;
         ALTER TABLE tagcounts ALTER COLUMN "weightedCount" SET NOT NULL;
    """,
    """\
         DROP TABLE profileconfig;
         ALTER TABLE tagcounts DROP COLUMN "weightedCount";
         ALTER TABLE services DROP COLUMN weight;
         ALTER TABLE users DROP COLUMN "weightedObjCount";
        
        delete from tagcounts;

        insert into tagcounts
        select user_id, tags_id, count(*)
        from (
          select ui.user_id, tui.tags_id
          from user_items ui join tags_useritems tui on ui.id = tui.user_items_id
          union all
          select ui.user_id, ti.tags_id
          from user_items ui join items on ui.item_id = items.id
           join tags_items ti on items.id = ti.items_id
        ) as alltags
        group by user_id, tags_id;


    """),
]

        
