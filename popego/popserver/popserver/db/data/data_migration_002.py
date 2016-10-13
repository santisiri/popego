"""Cargar Data inicial """

__docformat__ = "restructuredtext"


migration = [
    ("""\
INSERT INTO service_types ("type", description) VALUES ('photos', 'photo sharing services');
INSERT INTO services (name, description, url, agent, type_id, weight) VALUES ('Flickr', 'Flickr is a popular photo sharing service', 'http://flickr.com', 'popserver.agents.flickr_agent.FlickrAgent', (SELECT id FROM service_types WHERE "type" = 'photos'), 1);
INSERT INTO service_types ("type", description) VALUES ('videos', 'video sharing services');
INSERT INTO services (name, description, url, agent, type_id, weight) VALUES ('YouTube', 'YouTube is a popular video sharing service', 'http://www.youtube.com', 'popserver.agents.youtube_agent.YoutubeAgent', (SELECT id FROM service_types WHERE "type" = 'videos'), 1);
INSERT INTO service_types ("type", description, is_media) VALUES ('quotes', 'quote and micro-blogging services', FALSE);
INSERT INTO services (name, description, url, agent, type_id, weight) VALUES ('Twitter', 'Twitter is a free social networking and micro-blogging service that allows users to send short text-based posts', 'http://www.twitter.com', 'popserver.agents.twitter_agent.TwitterAgent', (SELECT id FROM service_types WHERE "type" = 'quotes'), 1);
INSERT INTO service_types ("type", description, is_media) VALUES ('bookmarks', 'Bookmarks and Links', TRUE);
INSERT INTO services (name, description, url, agent, type_id, weight) VALUES ('Del.icio.us', 'Del.icio.us is the first web2.0, it is all about bookmarks', 'http://del.icio.us', 'popserver.agents.delicious_agent.DeliciousAgent', (SELECT id FROM service_types WHERE "type" = 'bookmarks'), 1);
INSERT INTO service_types (type, description, is_media) VALUES ('music', 'last.fm alikes', TRUE);
INSERT INTO services (name, description, url, agent, type_id, weight) VALUES ('Last.fm', 'Last.fm taps the wisdom of the crowds, leveraging each user musical profile to make personalised recommendations', 'http://www.last.fm', 'popserver.agents.lastfm_agent.LastFmAgent', (SELECT id FROM service_types WHERE "type" = 'music'), 1);
INSERT INTO profileconfig VALUES (1, 1.0, 0.5, 1.0, 1.0); 
INSERT INTO globalconfig VALUES('current_profile_config', '1');

SELECT calculate_all(1);
     """, 
     """\
        DELETE FROM globalconfig;
        DELETE FROM profileconfig;
        DELETE FROM services WHERE name = 'Last.fm';
        DELETE FROM service_types WHERE "type" = 'music';
	      DELETE FROM services WHERE name = 'Del.icio.us';
        DELETE FROM service_types WHERE "type" = 'bookmarks';
        DELETE FROM services WHERE name = 'Twitter';
        DELETE FROM service_types WHERE "type" = 'quotes';
        DELETE FROM services WHERE name = 'Flickr';
        DELETE FROM service_types WHERE "type" = 'photos';
        DELETE FROM services WHERE name = 'YouTube';
        DELETE FROM service_types WHERE "type" = 'videos';

     """)
]
