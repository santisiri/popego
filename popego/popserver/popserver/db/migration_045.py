# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 042
# Delete orphans

migration = [
    ("""\
        -- Delete orphan user items
        CREATE OR REPLACE FUNCTION check_orphan_useritems() RETURNS TRIGGER AS $check_orphan_useritems$
          BEGIN
            if (select count(*) from itemgroups_items where user_items_id = OLD.user_items_id) = 0 then
              delete from user_items where id = OLD.user_items_id;
            end if;

            RETURN NULL;
          END;
        $check_orphan_useritems$ LANGUAGE plpgsql;


        CREATE TRIGGER check_orphan_useritems AFTER DELETE ON itemgroups_items 
             FOR EACH ROW EXECUTE PROCEDURE check_orphan_useritems();  


        -- Delete orphan items
        CREATE OR REPLACE FUNCTION check_orphan_items() RETURNS TRIGGER AS $check_orphan_items$
          BEGIN
            if (select count(*) from user_items where item_id = OLD.item_id) = 0 then
              delete from items where id = OLD.item_id;
            end if;

            RETURN NULL;
          END;
        $check_orphan_items$ LANGUAGE plpgsql;


        -- Los triggers al mismo evento en la misma tabla se ejecutan en orden alfabetico
        DROP TRIGGER sync_useritem ON user_items;

        CREATE TRIGGER a_sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();


        CREATE TRIGGER m_check_orphan_items AFTER DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE check_orphan_items();  

     """, 
     """\
        DROP TRIGGER m_check_orphan_items ON user_items;
        DROP TRIGGER a_sync_useritem ON user_items;
        CREATE TRIGGER sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();
        DROP FUNCTION check_orphan_items();
        DROP TRIGGER check_orphan_useritems ON itemgroups_items;
        DROP FUNCTION check_orphan_useritems(); 
     """),
]

