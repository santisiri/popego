# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# factories

migration = [
    ("""
         UPDATE services 
           SET item_factory='popserver.sync.item_factory:YoutubeUserItemFactory'
           WHERE name = 'YouTube';
         UPDATE services 
           SET item_factory='popserver.sync.item_factory:FlickrUserItemFactory'
           WHERE name = 'Flickr';
         UPDATE services 
           SET item_factory='popserver.sync.item_factory:DeliciousUserItemFactory'
           WHERE name = 'Del.icio.us';
         UPDATE services 
           SET item_factory='popserver.sync.item_factory:LastFMUserItemFactory'
           WHERE name = 'Last.fm';
     """, 
     """
        SELECT 1;
     """),
]

