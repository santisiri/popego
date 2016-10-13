# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
        -- Dado un usuario (user_id), tag (tag_id) y codigo de operacion (INSERT o DELETE) 
        -- actualiza la tabla tagcouts
        CREATE OR REPLACE FUNCTION update_tagcount(p_user_id users.id%%TYPE, p_tag_id integer, p_operation VARCHAR, 
                              p_weightedCount real) 
         RETURNS VOID AS $update_tagcount$
          DECLARE 
            tagcount integer;
          BEGIN
            IF p_operation = 'INSERT' THEN
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then 
                insert into tagcounts(user_id, tag_id, count, "weightedCount") values (p_user_id, p_tag_id, 1, p_weightedCount);
              else
                update tagcounts set count = count + 1, "weightedCount" = "weightedCount" + p_weightedCount
                 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            ELSE
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then 
                raise exception 'missing tagcount (user_id: %%, tag_id: %%)', p_user_id, p_tag_id;
              elsif tagcount = 1 then
                delete from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              else
                update tagcounts set count = count - 1, "weightedCount" = "weightedCount" - p_weightedCount 
                 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            END IF;
          END;
        $update_tagcount$ LANGUAGE plpgsql;


        -- Actualiza tagcounts en base a las altas y bajas de tags en user_items
        CREATE OR REPLACE FUNCTION sync_useritem_tags() RETURNS TRIGGER AS $sync_useritem_tags$
          DECLARE 
            l_user_id  integer;
            l_tag_id  integer;
            l_user_item_id integer;
            l_item_id integer;
            l_has_item_tag boolean;
            l_tag_weight real;
            l_ui_tag_weight real;
          BEGIN
            if TG_OP = 'INSERT' then 
              l_tag_id := NEW.tags_id;
              l_user_item_id := NEW.user_items_id;
            else
              l_tag_id := OLD.tags_id;
              l_user_item_id := OLD.user_items_id;
              -- Si se borra porque se borro el padre (cascade) ya fue procesado por este.
              if (select count(*) from user_items where id = l_user_item_id) = 0 then
                RETURN NULL;
              end if;
            end if;

            select into l_user_id, l_item_id  user_id, item_id  from user_items where user_items.id = l_user_item_id;
            l_has_item_tag := (select tags_id from tags_items where tags_id = l_tag_id and items_id = l_item_id) is not null;
            select into l_ui_tag_weight weigh_user_item_tag(l_user_item_id);
            
            if TG_OP = 'INSERT' then 
              if l_has_item_tag then 
                select into l_tag_weight weigh_item_tag(l_item_id);
                perform update_tagcount(l_user_id, l_tag_id, 'DELETE', l_tag_weight);
              end if;
              perform update_tagcount(l_user_id, l_tag_id, 'INSERT', l_ui_tag_weight);
            else
              perform update_tagcount(l_user_id, l_tag_id, 'DELETE', l_ui_tag_weight);
              if l_has_item_tag then 
                select into l_tag_weight weigh_item_tag(l_item_id);
                perform update_tagcount(l_user_id, l_tag_id, 'INSERT', l_tag_weight);
              end if;
            end if;

            RETURN NULL;
          END;
        $sync_useritem_tags$ LANGUAGE plpgsql;



        -- Actualiza tagcounts en base a las altas y bajas de tags en items
        -- 
        -- DELETE: Si se borra la tupla sola, es correcto. Si es por un cascade
        -- no va a haber user_items con el item padre con lo cual no se borra nada
        -- y es correcto.
        CREATE OR REPLACE FUNCTION sync_item_tags() RETURNS TRIGGER AS $sync_item_tags$
          DECLARE 
            l_user_id  integer;
            l_item_id  integer;
            l_tag_id  integer;
            l_tag_weight real;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_item_id := NEW.items_id;
              l_tag_id := NEW.tags_id;
            ELSE
              l_item_id := OLD.items_id;
              l_tag_id := OLD.tags_id;
            END IF;
            
            select into l_tag_weight weigh_item_tag(l_item_id);

            FOR l_user_id IN
              SELECT user_id 
              FROM user_items
              WHERE item_id = l_item_id
               AND id NOT IN (select user_items_id from tags_useritems 
                              where tags_id = l_tag_id)
            LOOP
              PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);   
            END LOOP;

            RETURN NULL;
          END;
        $sync_item_tags$ LANGUAGE plpgsql;



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
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_items 
                WHERE items_id = l_item_id
                AND tags_id NOT IN (select tags_id from tags_useritems
                              where user_items_id = l_user_item_id)
              LOOP
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
              END LOOP;

              -- Borro tags asociados al useritem.
              FOR l_tag_id IN
                SELECT tags_id 
                FROM tags_useritems 
                WHERE user_items_id = l_user_item_id
              LOOP
                PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_ui_tag_weight);
              END LOOP;
              
            end if;

            select into l_item_weight weigh_item(l_item_id);
            PERFORM update_object_count(l_user_id, l_item_weight, TG_OP);

            RETURN NULL;
          END;
        $sync_useritem$ LANGUAGE plpgsql;



    """,
    """\
        -- Ante un alta o baja de un UserItem agrega/borra los tags asociados al Item
        -- del UserItem
        -- Los tags del UserItem son manejados por sync_useritem_tags
        CREATE OR REPLACE FUNCTION sync_useritem() RETURNS TRIGGER AS $sync_useritem$
          DECLARE
            l_user_id  integer;
            l_item_id  integer;
            l_tag_id  integer;
            l_tag_weight real;
            l_item_weight real;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_item_id := NEW.item_id;
              l_user_id := NEW.user_id;
            ELSE
              l_item_id := OLD.item_id;
              l_user_id := OLD.user_id;
            END IF;

            select into l_tag_weight weigh_item_tag(l_item_id);

            FOR l_tag_id IN
              SELECT tags_id
              FROM tags_items
              WHERE items_id = l_item_id
            LOOP
              PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP, l_tag_weight);
            END LOOP;

            select into l_item_weight weigh_item(l_item_id);
            PERFORM update_object_count(l_user_id, l_item_weight, TG_OP);

            RETURN NULL;
          END;
        $sync_useritem$ LANGUAGE plpgsql;

        -- Actualiza tagcounts en base a las altas y bajas de tags en items
        CREATE OR REPLACE FUNCTION sync_item_tags() RETURNS TRIGGER AS $sync_item_tags$
          DECLARE
            l_user_id  int;
            l_item_id  int;
            l_tag_id  int;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_item_id := NEW.items_id;
              l_tag_id := NEW.tags_id;
            ELSE
              l_item_id := OLD.items_id;
              l_tag_id := OLD.tags_id;
            END IF;

            FOR l_user_id IN
              SELECT user_id
              FROM user_items
              WHERE item_id = l_item_id
            LOOP
              PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP);
            END LOOP;

            RETURN NULL;
          END;
        $sync_item_tags$ LANGUAGE plpgsql;


        -- Actualiza tagcounts en base a las altas y bajas de tags en user_items
        CREATE OR REPLACE FUNCTION sync_useritem_tags() RETURNS TRIGGER AS $sync_useritem_tags$
          DECLARE
            l_user_id  integer;
            l_tag_id  integer;
            l_user_item_id integer;
            l_item_id integer;
            l_has_item_tag boolean;
            l_tag_weight real;
            l_ui_tag_weight real;
          BEGIN
            if TG_OP = 'INSERT' then
              l_tag_id := NEW.tags_id;
              l_user_item_id := NEW.user_items_id;
            else
              l_tag_id := OLD.tags_id;
              l_user_item_id := OLD.user_items_id;
            end if;
            select into l_user_id, l_item_id  user_id, item_id  from user_items where user_items.id = l_user_item_id;
            l_has_item_tag := (select tags_id from tags_items where tags_id = l_tag_id and items_id = l_item_id) is not null;
            select into l_ui_tag_weight weigh_user_item_tag(l_user_item_id);

            if TG_OP = 'INSERT' then
              if l_has_item_tag then
                select into l_tag_weight weigh_item_tag(l_item_id);
                perform update_tagcount(l_user_id, l_tag_id, 'DELETE', l_tag_weight);
              end if;
              perform update_tagcount(l_user_id, l_tag_id, 'INSERT', l_ui_tag_weight);
            else
              perform update_tagcount(l_user_id, l_tag_id, 'DELETE', l_ui_tag_weight);
              if l_has_item_tag then
                select into l_tag_weight weigh_item_tag(l_item_id);
                perform update_tagcount(l_user_id, l_tag_id, 'INSERT', l_tag_weight);
              end if;
            end if;

            RETURN NULL;
          END;
        $sync_useritem_tags$ LANGUAGE plpgsql;



        -- Dado un usuario (user_id), tag (tag_id) y codigo de operacion (INSERT o DELETE)
        -- actualiza la tabla tagcouts
        CREATE OR REPLACE FUNCTION update_tagcount(p_user_id users.id%%TYPE, p_tag_id integer, p_operation VARCHAR,
                              p_weightedCount real)
         RETURNS VOID AS $update_tagcount$
          DECLARE
            tagcount integer;
          BEGIN
            IF p_operation = 'INSERT' THEN
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then
                insert into tagcounts(user_id, tag_id, count, "weightedCount") values (p_user_id, p_tag_id, 1, p_weightedCount);
              else
                update tagcounts set count = count + 1, "weightedCount" = "weightedCount" + p_weightedCount
                 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            ELSE
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then
                raise exception 'missing tagcount';
              elsif tagcount = 1 then
                delete from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              else
                update tagcounts set count = count - 1, "weightedCount" = "weightedCount" - p_weightedCount
                 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            END IF;
          END;
        $update_tagcount$ LANGUAGE plpgsql;
    """),
]



        
