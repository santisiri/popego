# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('', controller='website/home')

    # LOGIN, SIGNUP, SIGNOUT ROUTES
    map.connect('login', controller='website/home')
    map.connect('signup', controller='website/users')
    map.connect('signin', 'signin', controller='auth', action='signin')
    map.connect('signout', 'signout', controller='auth', action='signout')

    # ABOUT ROUTES
    map.connect('about/:action', controller='website/about')
    map.connect('about/feedback', controller='website/about', action='feedback')

    # This is to avoid controller errors due to inexistent users
    map.connect(':username', controller='website/users', action='home')

    # USER PAGES ROUTES
    # Home, Social Feed, Stats, Services, Widgets, Settings
    map.connect(':username/home', controller='website/users', action='home')
    map.connect(':username/socialfeed', controller='website/socialfeed')
    map.connect(':username/services', controller='website/service')
    map.connect(':username/services/:action/:id', 
		    controller='website/service', action='index')
    map.connect(':username/services/toptags', 
                controller='website/service', action='toptags')
    map.connect(':username/widgets', controller='website/widgets')
    map.connect(':username/widgets/:id/theme', 
                controller='website/widgets', action='theme',
                conditions=dict(method=['POST']))
    map.connect(':username/stats', controller='website/stats')
    map.connect(':username/settings', controller='website/settings')
    map.connect(':username/settings/avatar/upload', 
                controller='website/settings', action='upload')
    map.connect(':username/settings/personal', 
                controller='website/settings', action='personal_settings')
    map.connect(':username/settings/password', 
                controller='website/settings', action='password_settings')

    map.connect(':username/tag_interest/:tag',
                controller='website/interests', action='setTagInterest')

    map.connect(':username/feedback', controller='website/about', 
                action='user_feedback')

    # MEDIA ROUTES
    map.connect(':username/api/items/:itemtype/:group', 
                controller='widget/items', action='items', group=None)
    map.connect(':username/api/groups/:itemtype', 
                controller='widget/items', action='groups')
    # the following media routes may be deprecated:
    map.connect(':username/api/pictures/albums/:page', 
                controller='widget/media', action='picturesGroups', page=1)
    map.connect(':username/api/pictures/:groupId/:page', 
                controller='widget/media', action='picturesThumbs', page=1)
    map.connect(':username/api/pictures/:groupId/pic/:itemId', 
                controller='widget/media', action='picturesShowcase')
    
    map.connect(':username/api/videos/albums/:page', 
                controller='widget/media', action='videosGroups', page=1)
    map.connect(':username/api/videos/:groupId/:page', 
                controller='widget/media', action='videosThumbs', page=1)
    map.connect(':username/api/videos/:groupId/v/:itemId', 
                controller='widget/media', action='videosShowcase')

    map.connect(':username/api/bookmarks/:page', 
                controller='widget/media', action='bookmarks')

    map.connect(':username/api/music/:page',
                controller='widget/media', action='music')
    
    map.connect(':username/api/music/ranks/:rank/:page',
                controller='widget/media', action='musicRanks')
    
    # WIDGET ROUTES
    map.connect('widget_bootstrap',':username/api/widget/:id',
                controller='widget/widget', action='show', 
                requirements=dict(id='\d+'))
    map.connect('onsite_widget_bootstrap',':username/api/onsitewidget/:id',
                controller='widget/widget', action='onsiteShow', 
                requirements=dict(id='\d+'))
    map.connect(':username/api/widget/:id/content', 
                controller='widget/widget', action='content', 
                requirements=dict(id='\d+'))
    map.connect('popcard_section',':username/api/widget/:id/:action',
                controller='widget/widget', 
                requirements=dict(id='\d+'))

    
    map.connect(':controller/:action/:id')

    map.connect('*url', controller='template', action='view')

    return map

