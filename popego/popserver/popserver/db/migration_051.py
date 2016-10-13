# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
        DROP TRIGGER a_sync_useritem ON user_items;


        -- Ante un alta de UserItem agrega los tags asociados al Item
        -- del UserItem. Los tags del UserItem son manejados por sync_useritem_tags
        --
        -- Ante una baja de UserItem borra los tags asociados al Item que no 
        -- esten en el UserItem y borra todos los tags del UserItem (esto ultimo es
        -- asi porque aunque haya un on delete cascade, la tupla padre se borra y 
        -- luego ejecutaria un trigger sobre la tupla hija). Ver
        -- http://archives.postgresql.org/pgsql-general/2002-11/msg01110.php por detalles.
        CREATE OR REPLACE FUNCTION sync_useritem() RETURNS TRIGGER AS $sync_useritem$
          DECLARE 
            l_user_item_id integer;
            l_user_id  integer;
            l_item_id  integer;
            l_tag_id  integer;
            l_tag_weight real;
            l_item_weight real;
            l_ui_tag_weight real;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_user_item_id := NEW.id;
              l_item_id := NEW.item_id;
              l_user_id := NEW.user_id;
            ELSE
              l_user_item_id := OLD.id;
              l_item_id := OLD.item_id;
              l_user_id := OLD.user_id;
            END IF;

            select into l_tag_weight weigh_item_tag(l_item_id);
            select into l_ui_tag_weight weigh_user_item_tag(l_user_item_id);

            if TG_OP = 'INSERT' then
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_items 
                WHERE items_id = l_item_id
              LOOP
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
              END LOOP;
            else 
              -- Borro tags asociados al item que no estan en el useritem.

              -- DEBUG 
               raise notice 'sync_useritem: por borrar itemtags';

              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_items 
                WHERE items_id = l_item_id
                AND tags_id NOT IN (select tags_id from tags_useritems
                              where user_items_id = l_user_item_id)
              LOOP
                -- DEBUG 
               raise notice 'sync_useritem: borrando itemtag %%', l_tag_id;
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
              END LOOP;

              -- Borro tags asociados al useritem.
                -- DEBUG 
               raise notice 'sync_useritem: por borrar user_itemtags';
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_useritems 
                WHERE user_items_id = l_user_item_id
              LOOP
                -- DEBUG 
               raise notice 'sync_useritem: borrando useritem_tag %%', l_tag_id;
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_ui_tag_weight);
              END LOOP;
              
            end if;

            select into l_item_weight weigh_item(l_item_id);
            PERFORM update_object_count(l_user_id, l_item_weight, TG_OP);

            if TG_OP = 'INSERT' then
                RETURN NULL;
            else
                RETURN OLD;
            end if;
          END;
        $sync_useritem$ LANGUAGE plpgsql;

        CREATE TRIGGER a_sync_useritem_deletion BEFORE DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();
        
        CREATE TRIGGER a_sync_useritem_insertion AFTER INSERT ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();




    """,
    """\
        DROP TRIGGER a_sync_useritem_deletion ON user_items;
        DROP TRIGGER a_sync_useritem_insertion ON user_items;

        -- Ante un alta de UserItem agrega los tags asociados al Item
        -- del UserItem. Los tags del UserItem son manejados por sync_useritem_tags
        --
        -- Ante una baja de UserItem borra los tags asociados al Item que no 
        -- esten en el UserItem y borra todos los tags del UserItem (esto ultimo es
        -- asi porque aunque haya un on delete cascade, la tupla padre se borra y 
        -- luego ejecutaria un trigger sobre la tupla hija). Ver
        -- http://archives.postgresql.org/pgsql-general/2002-11/msg01110.php por detalles.
        CREATE OR REPLACE FUNCTION sync_useritem() RETURNS TRIGGER AS $sync_useritem$
          DECLARE 
            l_user_item_id integer;
            l_user_id  integer;
            l_item_id  integer;
            l_tag_id  integer;
            l_tag_weight real;
            l_item_weight real;
            l_ui_tag_weight real;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_user_item_id := NEW.id;
              l_item_id := NEW.item_id;
              l_user_id := NEW.user_id;
            ELSE
              l_user_item_id := OLD.id;
              l_item_id := OLD.item_id;
              l_user_id := OLD.user_id;
            END IF;

            select into l_tag_weight weigh_item_tag(l_item_id);
            select into l_ui_tag_weight weigh_user_item_tag(l_user_item_id);

            if TG_OP = 'INSERT' then
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_items 
                WHERE items_id = l_item_id
              LOOP
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
              END LOOP;
            else 
              -- Borro tags asociados al item que no estan en el useritem.

              -- DEBUG 
               raise notice 'sync_useritem: por borrar itemtags';

              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_items 
                WHERE items_id = l_item_id
                AND tags_id NOT IN (select tags_id from tags_useritems
                              where user_items_id = l_user_item_id)
              LOOP
                -- DEBUG 
               raise notice 'sync_useritem: borrando itemtag %%', l_tag_id;
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
              END LOOP;

              -- Borro tags asociados al useritem.
                -- DEBUG 
               raise notice 'sync_useritem: por borrar user_itemtags';
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_useritems 
                WHERE user_items_id = l_user_item_id
              LOOP
                -- DEBUG 
               raise notice 'sync_useritem: borrando useritem_tag %%', l_tag_id;
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_ui_tag_weight);
              END LOOP;
              
            end if;

            select into l_item_weight weigh_item(l_item_id);
            PERFORM update_object_count(l_user_id, l_item_weight, TG_OP);

            RETURN NULL;
          END;
        $sync_useritem$ LANGUAGE plpgsql;
        
        CREATE TRIGGER a_sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();

    """),
]



        
