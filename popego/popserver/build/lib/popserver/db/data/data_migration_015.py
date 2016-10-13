"""Cargar Data inicial """

__docformat__ = "restructuredtext"


migration = [
    ("""\
	UPDATE services SET item_factory = 'popserver.sync.item_factory:TwitterUserItemFactory' WHERE name = 'Twitter';
	INSERT INTO service_types ("type", description) VALUES ('blogs', 'blog services');
	INSERT INTO services (name, description, url, agent, type_id, item_factory, weight, prompt_text, added_text) VALUES ('Blog', 'A generic service for any blog whose feed can be detected', '', 'popserver.agents.blog_agent', (SELECT id FROM service_types WHERE "type" = 'blogs'), 'popserver.sync.item_factory:BlogUserItemFactory', 1, 'blog url:', 'added blog');
     """, 
     """\
        DELETE FROM services WHERE name = 'Blog';
        DELETE FROM service_types WHERE "type" = 'blogs';
	UPDATE services SET item_factory = NULL WHERE name = 'Twitter';
     """)
]
