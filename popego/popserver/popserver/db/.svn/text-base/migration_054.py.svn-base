# -*- coding: utf-8 -*-
""" """
__docformat__ = "restructuredtext"


migration = [
    ("""\
        -- Previene que se borre un artist si hay alguna song que lo refiere.
        -- Un artista puede borrarse si quedo huerfano de user_items (check_orphan_items).
        -- Este trigger se complementa con remove_orphan_artist 
        CREATE OR REPLACE FUNCTION prevent_artist_removal() RETURNS TRIGGER AS $prevent_artist_removal$
          DECLARE 
          BEGIN
            if OLD.row_type = 'artist' and (select count(*) from songs where artist_item_id = OLD.id) > 0 then
                return NULL;
            else
                return OLD;
            end if;
          END;
        $prevent_artist_removal$ LANGUAGE plpgsql;

        CREATE TRIGGER prevent_artist_removal BEFORE DELETE ON items
         FOR EACH ROW EXECUTE PROCEDURE prevent_artist_removal();


        -- Borra un artista si quedo huerfano de songs y user_items
        -- Este trigger se complementa con prevent_artist_removal
        CREATE OR REPLACE FUNCTION remove_orphan_artist() RETURNS TRIGGER AS $remove_orphan_artist$
          DECLARE 
          BEGIN
            if (select count(*) from songs where artist_item_id = OLD.artist_item_id) = 0 and
               (select count(*) from user_items where item_id = OLD.artist_item_id) = 0    
            then
                delete from items where id = OLD.artist_item_id;
            end if;

            return NULL;
          END;
        $remove_orphan_artist$ LANGUAGE plpgsql;

        CREATE TRIGGER remove_orphan_artist AFTER DELETE ON songs
         FOR EACH ROW EXECUTE PROCEDURE remove_orphan_artist();
    """,
    """\
        DROP TRIGGER remove_orphan_artist ON songs;
        DROP FUNCTION remove_orphan_artist();
        DROP TRIGGER prevent_artist_removal ON items;
        DROP FUNCTION prevent_artist_removal();
    """),
]



        
