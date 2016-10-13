# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 028
# Cambio de naming para agentes

migration = [
    ("""
        UPDATE services 
           SET agent='popserver.agents.lastfm_agent:LastFmAgent()'
           WHERE agent = 'popserver.agents.lastfm_agent.LastFmAgent';
        UPDATE services 
           SET agent='popserver.agents.youtube_agent'
           WHERE agent = 'popserver.agents.youtube_agent.YoutubeAgent';
        UPDATE services 
           SET agent='popserver.agents.flickr_agent:FlickrAgent()'
           WHERE agent = 'popserver.agents.flickr_agent.FlickrAgent';
        UPDATE services 
           SET agent='popserver.agents.twitter_agent:TwitterAgent()' 
           WHERE agent = 'popserver.agents.twitter_agent.TwitterAgent';
        UPDATE services 
           SET agent='popserver.agents.delicious_agent'
           WHERE agent = 'popserver.agents.delicious_agent.DeliciousAgent';
     """, 
     """
        UPDATE services 
           SET agent = 'popserver.agents.lastfm_agent.LastFmAgent'
           WHERE agent='popserver.agents.lastfm_agent:LastFmAgent()';
        UPDATE services 
           SET agent = 'popserver.agents.youtube_agent.YoutubeAgent'
           WHERE agent='popserver.agents.youtube_agent';
        UPDATE services 
           SET agent='popserver.agents.flickr_agent:FlickrAgent()'
           WHERE agent = 'popserver.agents.flickr_agent.FlickrAgent';
        UPDATE services 
           SET agent = 'popserver.agents.twitter_agent.TwitterAgent'
           WHERE agent='popserver.agents.twitter_agent:TwitterAgent()';
        UPDATE services 
           SET agent = 'popserver.agents.delicious_agent.DeliciousAgent'
           WHERE agent='popserver.agents.delicious_agent';
     """),
]

