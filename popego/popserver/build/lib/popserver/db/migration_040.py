# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
        DROP FUNCTION update_tagcount(integer, integer, VARCHAR);

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



        CREATE OR REPLACE FUNCTION get_uItemTagWeight()
          RETURNS profileconfig."uItemTagWeight"%%TYPE AS $get_uItemTagWeight$
         DECLARE
            ret profileconfig."uItemTagWeight"%%TYPE;
         BEGIN
          select into ret "uItemTagWeight" 
          from profileconfig
          where id = (select cast(value as integer) from globalconfig where property = 'current_profile_config');
          
          RETURN ret;
         END;
        $get_uItemTagWeight$ LANGUAGE plpgsql;


        CREATE OR REPLACE FUNCTION get_itemTagWeight()
          RETURNS profileconfig."itemTagWeight"%%TYPE AS $get_itemTagWeight$
         DECLARE
            ret profileconfig."itemTagWeight"%%TYPE;
         BEGIN
          select into ret "itemTagWeight" 
          from profileconfig
          where id = (select cast(value as integer) from globalconfig where property = 'current_profile_config');
          
          RETURN ret;
         END;
        $get_itemTagWeight$ LANGUAGE plpgsql;



        CREATE OR REPLACE FUNCTION weigh_user_item_tag(p_user_item_id integer) 
          RETURNS real AS $weigh_user_item_tag$
         DECLARE
          l_service_weight real;
          uItemTagWeight profileconfig."uItemTagWeight"%%TYPE;
         BEGIN
          select into l_service_weight weight 
          from user_items ui join items i on ui.item_id = i.id
           join services s on i.service_id = s.id
          where ui.id =  p_user_item_id;
          
          select into uItemTagWeight get_uItemTagWeight();

          return uItemTagWeight * l_service_weight;
         END;
        $weigh_user_item_tag$ LANGUAGE plpgsql;



        CREATE OR REPLACE FUNCTION weigh_item_tag(p_item_id integer) 
          RETURNS real AS $weigh_item_tag$
         DECLARE
          l_service_weight real;
          itemTagWeight profileconfig."itemTagWeight"%%TYPE;
         BEGIN
          select into l_service_weight weight 
          from items i join services s on i.service_id = s.id
          where i.id =  p_item_id;
          
          select into itemTagWeight get_itemTagWeight();

          return itemTagWeight * l_service_weight;
         END;
        $weigh_item_tag$ LANGUAGE plpgsql;



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


        DROP TRIGGER sync_useritem_tags ON tags_useritems;


        CREATE TRIGGER sync_useritem_tags AFTER INSERT OR DELETE ON tags_useritems
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem_tags();  


        -- Acutualiza tagcounts en base a las altas y bajas de tags en items
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


        DROP TRIGGER sync_item_tags ON tags_items;

        CREATE TRIGGER sync_item_tags AFTER INSERT OR DELETE ON tags_items
             FOR EACH ROW EXECUTE PROCEDURE sync_item_tags();  



        CREATE OR REPLACE FUNCTION weigh_item(p_item_id integer) 
          RETURNS real AS $weigh_item$
         DECLARE
          l_service_weight real;
         BEGIN
          select into l_service_weight weight 
          from items i join services s on i.service_id = s.id
          where i.id =  p_item_id;
          
          return l_service_weight;
         END;
        $weigh_item$ LANGUAGE plpgsql;


        -- Dado un usuario (user_id), peso del objecto (item_weight) y codigo de operacion (INSERT o DELETE) 
        -- actualiza la tabla users con el peso sumarizado de los objetos.
        CREATE OR REPLACE FUNCTION update_object_count(p_user_id integer, p_item_weight real, 
                                                        p_operation VARCHAR) 
         RETURNS VOID AS $update_object_count$
          DECLARE 
            l_effective_item_weight real;
          BEGIN
            l_effective_item_weight := p_item_weight;
            IF p_operation = 'DELETE' THEN
              l_effective_item_weight := l_effective_item_weight * -1;
            END IF;
            
            update users set "weightedObjCount" = "weightedObjCount" + l_effective_item_weight
             where id = p_user_id;
          END;
        $update_object_count$ LANGUAGE plpgsql;



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


        DROP TRIGGER sync_useritem ON user_items;

        CREATE TRIGGER sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();  

        
        -- Inicializa con los datos existentes.

        -- Agrega los tags de user_items y los de item.

        CREATE OR REPLACE FUNCTION calculate_tagcounts() 
         RETURNS VOID AS $calculate_tagcounts$
          BEGIN
          delete from tagcounts;
          
          insert into tagcounts
          select user_id, tags_id, count(*), 0
          from (
              select ui.user_id, tui.tags_id
              from user_items ui join tags_useritems tui on ui.id = tui.user_items_id
              union all
              select ui.user_id, ti.tags_id
              from user_items ui join items on ui.item_id = items.id 
              join tags_items ti on items.id = ti.items_id
              where ti.tags_id not in (
                       select tags_id 
                       from tags_useritems
                       where tags_useritems.user_items_id = ui.id
              )
          ) as alltags
          group by user_id, tags_id;
          END;
        $calculate_tagcounts$ LANGUAGE plpgsql;



        CREATE OR REPLACE FUNCTION calculate_weighted_tagcounts(profileconfig_id integer) 
         RETURNS VOID AS $calculate_weighted_tagcounts$
          BEGIN
            IF (select id from profileconfig where profileconfig_id = id) is NULL THEN
              RAISE EXCEPTION 'profileconfig does not exist';
            END IF; 
          
          update tagcounts set "weightedCount" = 0;
          
          update tagcounts tc set "weightedCount" = (
                  select coalesce(sum(wc), 0)
                  from (
                    -- Sumarizo en forma pesada los tags de UserItems
                    select count(*) * s.weight * pc."uItemTagWeight" as wc
                    from user_items ui join tags_useritems tui on ui.id = tui.user_items_id
                      join items i on i.id = ui.item_id
                      join services s on s.id = i.service_id, profileconfig pc
                    where ui.user_id = tc.user_id
                     and tui.tags_id = tc.tag_id
                     and pc.id = profileconfig_id
                    group by s.id, s.weight, pc."uItemTagWeight"
                    union all
                    -- Sumarizo en forma pesada a los tags de Items.
                    -- No se tiene en cuenta el tag si ya esta presente en tags_useritems
                    -- para este UserItem.
                    select count(*) * s.weight * pc."itemTagWeight" as wc
                    from items i join tags_items ti on i.id = ti.items_id
                      join user_items ui on i.id = ui.item_id
                      join services s on s.id = i.service_id, profileconfig pc
                    where ui.user_id = tc.user_id
                     and ti.tags_id = tc.tag_id
                     and pc.id = profileconfig_id
                     and ti.tags_id not in (
                       select tags_id 
                       from tags_useritems
                       where tags_useritems.user_items_id = ui.id
                     )
                    group by s.id, s.weight, pc."itemTagWeight"
                  ) as wcs
          );
          END;
        $calculate_weighted_tagcounts$ LANGUAGE plpgsql;


        CREATE OR REPLACE FUNCTION calculate_weighted_userobjects() 
         RETURNS VOID AS $calculate_weighted_userobjects$
          BEGIN
          update users set "weightedObjCount" = 0;
          
          update users u set "weightedObjCount" = (
            select coalesce(sum(sc), 0)
            from (
             select count(*) * s.weight as sc
             from user_items ui join items i on ui.item_id = i.id
               join services s on i.service_id = s.id
             where ui.user_id = u.id
             group by s.id, s.weight
            ) as scs
          );
          END;
        $calculate_weighted_userobjects$ LANGUAGE plpgsql;


        CREATE OR REPLACE FUNCTION calculate_all(profileconfig_id integer)
         RETURNS VOID AS $calculate_all$
          BEGIN
            PERFORM calculate_tagcounts();
            PERFORM calculate_weighted_tagcounts(profileconfig_id);
            PERFORM calculate_weighted_userobjects();
          END;
        $calculate_all$ LANGUAGE plpgsql;
    """,
    """\
        DROP FUNCTION calculate_all(integer);
        DROP FUNCTION calculate_weighted_userobjects();
        DROP FUNCTION calculate_weighted_tagcounts(integer);
        DROP FUNCTION calculate_tagcounts();
        DROP FUNCTION update_tagcount(integer, integer, VARCHAR, real);
        DROP FUNCTION get_uItemTagWeight();
        DROP FUNCTION get_itemTagWeight();
        DROP FUNCTION weigh_user_item_tag(integer);
        DROP FUNCTION weigh_item_tag(integer);
        DROP FUNCTION weigh_item(integer);
        DROP FUNCTION update_object_count(integer, real, VARCHAR);


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


        DROP TRIGGER sync_useritem_tags ON tags_useritems;

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

        
        DROP TRIGGER sync_item_tags ON tags_items;

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


        DROP TRIGGER sync_useritem ON user_items;

        CREATE TRIGGER sync_useritem AFTER INSERT OR DELETE ON user_items
             FOR EACH ROW EXECUTE PROCEDURE sync_useritem();  
    """),
]



        
