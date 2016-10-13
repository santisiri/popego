""" """

__docformat__ = "restructuredtext"

# Triggers de sumarizacion de tags
# Inicializacion de tagcounts en base a los datos presentes
# Requiere que el usuario que se conecta a la base tenga privilegios de superuser 
#  que funcione CREATE LANGUAGE

# TODO Ver como hacer para que DBApi acepte sentencias con % asi se puede usar
#  table.field%TYPE;

migration = [
    ("""\
        CREATE LANGUAGE 'plpgsql';  
      
        -- Dado un usuario (user_id), tag (tag_id) y codigo de operacion (INSERT o DELETE) 
        -- actualiza la tabla tagcouts
        CREATE OR REPLACE FUNCTION update_tagcount(p_user_id integer, p_tag_id integer, p_operation VARCHAR) 
         RETURNS INTEGER AS $update_tagcount$
          DECLARE 
            tagcount int;
          BEGIN
            IF p_operation = 'INSERT' THEN
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then 
                insert into tagcounts(user_id, tag_id, count) values (p_user_id, p_tag_id, 1);
              else
                update tagcounts set count = count + 1 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            ELSE
              select into tagcount count from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              if not found then 
                raise exception 'missing tagcount';
              elsif tagcount = 1 then
                delete from tagcounts where user_id = p_user_id and tag_id = p_tag_id;
              else
                update tagcounts set count = count - 1 where user_id = p_user_id and tag_id = p_tag_id;
              end if;
            END IF;

            RETURN NULL;
          END;
        $update_tagcount$ LANGUAGE plpgsql;


        -- Acutualiza tagcounts en base a las altas y bajas de tags en user_items
        CREATE OR REPLACE FUNCTION sync_useritem_tags() RETURNS TRIGGER AS $sync_useritem_tags$
          DECLARE 
            l_user_id  int;
            l_tag_id  int;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              select into l_user_id user_id from user_items where user_items.id = NEW.user_items_id;
              l_tag_id := NEW.tags_id;
            ELSE 
              select into l_user_id user_id from user_items where user_items.id = OLD.user_items_id;
              l_tag_id := OLD.tags_id;
            END IF;
          
            PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP);

            RETURN NULL;
          END;
        $sync_useritem_tags$ LANGUAGE plpgsql;




        CREATE TRIGGER sync_useritem_tags AFTER INSERT OR DELETE ON tags_useritems
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem_tags();  


        -- Acutualiza tagcounts en base a las altas y bajas de tags en items
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


        CREATE TRIGGER sync_item_tags AFTER INSERT OR DELETE ON tags_items
             FOR EACH ROW EXECUTE PROCEDURE sync_item_tags();  


        -- Ante un alta o baja de un UserItem agrega/borra los tags asociados al Item
        -- del UserItem
        -- Los tags del UserItem son manejados por sync_useritem_tags
        CREATE OR REPLACE FUNCTION sync_useritem() RETURNS TRIGGER AS $sync_useritem$
          DECLARE 
            l_user_id  int;
            l_item_id  int;
            l_tag_id  int;
          BEGIN
            IF TG_OP = 'INSERT' THEN
              l_item_id := NEW.item_id;
              l_user_id := NEW.user_id;
            ELSE
              l_item_id := OLD.item_id;
              l_user_id := OLD.user_id;
            END IF;

            FOR l_tag_id IN
              SELECT tags_id 
              FROM tags_items 
              WHERE items_id = l_item_id
            LOOP
              PERFORM update_tagcount(l_user_id, l_tag_id, TG_OP);   
            END LOOP;

            RETURN NULL;
          END;
        $sync_useritem$ LANGUAGE plpgsql;

        CREATE TRIGGER sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();  

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
    """,
    """\
      DELETE FROM tagcounts;
      DROP TRIGGER sync_useritem ON user_items;
      DROP FUNCTION sync_useritem();
      DROP TRIGGER sync_item_tags ON tags_items;
      DROP FUNCTION sync_item_tags();
      DROP TRIGGER sync_useritem_tags ON tags_useritems;
      DROP FUNCTION sync_useritem_tags();
      DROP FUNCTION update_tagcount(integer, integer, VARCHAR);
      DROP LANGUAGE 'plpgsql';  
    """),
]
