"""Cargar Data inicial """

__docformat__ = "restructuredtext"


migration = [
    ("""\
INSERT INTO services (name, description, url, agent, type_id, item_factory, weight, prompt_text, added_text) VALUES ('Picasa', 'Picasa is a popular photo sharing service', 'http://picasaweb.googlec..com', 'popserver.agents.picasa_agent', (SELECT id FROM service_types WHERE "type" = 'pictures'), 'popserver.sync.item_factory:FlickrUserItemFactory', 1, 'username:', 'added user');

     """, 
     """\
        DELETE FROM services WHERE name = 'Picasa';

     """)
]
