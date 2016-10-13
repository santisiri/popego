import logging
from popserver.ai.interest import tag as tagInterest
from popserver.lib.base import *
from popserver.lib.controller_utils import find_widget
from popserver.lib.util import interval_of_time_in_words
from datetime import datetime
from sqlalchemy.sql import or_
from sqlalchemy.orm import eagerload
from popserver.ai import compatibility
import sqlalchemy, elixir
import time
from routes import url_for

log = logging.getLogger(__name__)

ITEMS_COUNT_QUERY = sqlalchemy.text("""
 select st.type, coalesce(p.ct, 0) 
 from service_types st 
 left outer join 
 (select st.id, count(*) as ct 
  from user_items ui 
  join items i on ui.item_id = i.id 
  join services s on i.service_id = s.id 
  join service_types st on s.type_id = st.id
  where ui.user_id = :userid
  group by st.id) p 
 on p.id = st.id
""")



class WidgetController(BaseController):

    def home(self, username, id):
        widget = self._getWidget(username, id)
        c.user = widget.user
        t = self._getTheme(widget)
        c.theme = t["theme"]
        c.addThemeInReq = t["addInReq"]
    	qas = c.user.getAccountsByType(u'quotes')
    	c.myQuoteAccount = qas[0] if len(qas) else None

    	c.myServiceTypes = []
    	for st in ['pictures', 'videos']:
    		if self._hasServiceByType(c.user, st):
    			c.myServiceTypes.append(st)
    	c.myLastPhotos = self._getLastMediaByType('photo')
    	c.myLastVideos = self._getLastMediaByType('video')
    	c.remoteUser = self.user
        c.myTopTags = self._getTopTags(c.user)

        c.myAvatar = h.url_for_user_avatar(c.user)

        c.compatibility = None
        if self.user is not None:
            c.compatibility = compatibility.compatibilityFor(self.user, c.user)
    	return render('/widget/home/index.mako')

    def media(self, username, id):
        widget = self._getWidget(username, id)
        c.user = widget.user
        t = self._getTheme(widget)
        c.theme = t["theme"]
        c.addThemeInReq = t["addInReq"]
    	qas = c.user.getAccountsByType(u'quotes')
    	c.myQuoteAccount = qas[0] if len(qas) else None
        
        c.types = model.ServiceType.query.all() 
        c.typesCount = self._getUserItemsCount(c.user.id)

        return render('/widget/media/index.mako');


    def _getUserItemsCount(self, user_id):
        conn = elixir.metadata.bind.connect()
        results = conn.execute(ITEMS_COUNT_QUERY, userid=user_id).fetchall()
        return dict(results)

    def about(self, username, id):
        widget = self._getWidget(username, id)
        c.user = widget.user
        t = self._getTheme(widget)
        c.theme = t["theme"]
        c.addThemeInReq = t["addInReq"]
        c.baseUrl = self._getBaseUrl()
        return render('/widget/about/index.mako');
    
    def ranks(self, username):
        return 'TODO: Ranks'

    def scraps(self, username):
        return 'TODO: Scraps'

    def onsiteShow(self, username, id):
        return self._doShow(username, id, 'preview')

    def show(self, username, id):
        return self._doShow(username, id, 'default')

    def _getTheme(self, widget):
        theme = request.params.get('theme')
        r = {"addInReq": True if theme else False, "theme" : theme if theme else widget.getTheme()}
        return r

    def _doShow(self, username, id, display):
        """renders the JS needed for displaying the widget"""
        c.display = display
        widget = self._getWidget(username, id)
        c.widgetId = widget.id
        t = self._getTheme(widget)
        c.theme = t["theme"]
        c.addThemeInReq = t["addInReq"]
        c.username = username
        c.displayname = widget.user.displayname
        c.baseUrl = self._getBaseUrl()
        
        if c.display == 'default':
            response.content_type = 'text/javascript'

        return render('/widget/show.mako')

    def _getWidget(self, username, id):
        return find_widget(username, id)
            
    def content(self, username, id):
        """renders the contents of the iframe"""
        widget = self._getWidget(username, id)
        c.user = widget.user
        t = self._getTheme(widget)
        c.theme = t["theme"]
        c.addThemeInReq = t["addInReq"]
        c.myLastMedia = self._getLastMedia()
    	qas = c.user.getAccountsByType(u'quotes')
    	c.myQuoteAccount = qas[0] if len(qas) else None
        c.myTopTags = self._getTopTags(c.user)
        
        c.remoteUser = self.user
        c.remoteUserLoggedIn = self._isUserAuthenticated()
        c.baseUrl = self._getBaseUrl()
        # TODO Revisar si parentUrl y error se estan usando
        c.parentUrl = request.params.get('parentUrl') or '/'
        c.error = request.params.get('viewerLoginError') or False

        self._updatePopegosOfTheWorld(widget)

        c.myAvatar = h.url_for_user_avatar(c.user, 150)

        c.compatibility = None
        if self.user is not None:
            c.compatibility = compatibility.compatibilityFor(self.user, c.user)

        return render('/widget/content.mako')

    def _getLastMedia(self):
    	lastmedia =  model.dbsession.query(model.UserItem) \
            .filter(model.UserItem.user_id == c.user.id).join('item') \
    		.filter(or_(model.Item.row_type == 'photo', model.Item.row_type == 'video')) \
            .order_by(model.UserItem.creation_date.desc())[0:3].all()
    	return self._normalizeUserItems(lastmedia)

    def _getLastMediaByType(self, type):
    	lastmedia = model.dbsession.query(model.UserItem) \
            .filter(model.UserItem.user_id == c.user.id).join('item') \
            .filter(model.Item.row_type == type) \
            .order_by(model.UserItem.creation_date.desc())[0:6].all();
    	return self._normalizeUserItems(lastmedia)

    def _normalizeUserItems(self, useritems):
    	dictionaries = []
    	for useritem in useritems:
    		i = useritem.item
    		m = {}
    		m['title'] = i.title
    		m['description'] = i.description
    		if i.row_type == 'photo':
    			m['thumbnail'] = i.thumbnail_url
    			m['url'] = i.external_url
    		elif i.row_type == 'video':
    			m['thumbnail'] = i.thumbnails[0].url
    			m['url'] = i.externalURL
    		dictionaries.append(m)
    	return dictionaries

    def _hasServiceByType(self, user, type):
        """
        Decides whether the user has at least one service of the given type.
        """
        return model.dbsession.query(model.Account) \
            .filter(model.Account.user_id == user.id).join('service') \
            .filter(model.Service.type.has(model.ServiceType.type == type)).count() > 0

    def _getTopTags(self, user, n = 10):
        tagCounts = tagInterest.getUserTopInterests(user.id, n)
#         tagcounts = model.TagCount.query.options(eagerload('tag')) \
#             .filter(model.TagCount.user_id == user.id) \
#             .order_by(model.TagCount.count.desc())[0:n].all()
        return [t.tag.name for t in tagCounts]


    def _updatePopegosOfTheWorld(self, widget):
        ref = request.environ.get('HTTP_REFERER')
        host = 'http://' + request.environ.get('HTTP_HOST')
        if not ref or ref.find(host) == 0:
            return None

        widget.last_seen = datetime.now()
        widget.best_referrer = ref

        widget.flush()
        return widget

