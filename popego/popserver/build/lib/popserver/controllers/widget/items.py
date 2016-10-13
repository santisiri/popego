# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import logging
log = logging.getLogger(__name__)

from popserver.lib.base import *
from popserver.model import *

class ItemsController(BaseController):

	@jsonify
	def items(self, username, itemtype, group):
		try:
			p = self._get_params(username, itemtype)
		except ItemsControllerException, e:
			abort(404, e.message)
		items = self.items_by_group(p, group) \
				if group else self.items_all(p)
		return {'user': username, 'type': itemtype, 'group': group, \
				'count': p[3], 'offset': p[4], 'items': items}

	def items_all(self, p):
		(c.user, itemtype, stype, count, offset, tags) = p
		q =  UserItem.query.filter(UserItem.user_id == c.user.id) \
			.join('item').filter(Item.row_type == itemtype) \
			.order_by(UserItem.creation_date.desc())
		f = getattr(self, itemtype, None)
		useritems = q[offset:offset + count].all() if f else []
		return [f(i, self.item(i, tags)) for i in useritems]

	def items_by_group(self, p, group):
		(c.user, itemtype, stype, count, offset, tags) = p
		q = ItemGroup.query.join('account') \
			.filter(Account.user_id  == c.user.id) \
			.filter(ItemGroup.name == group)
		g = q.first() # TODO: eagerload de g.items
		f = getattr(self, itemtype, None)
		items = g.items[offset:offset + count] if g and f else []
		return [f(i, self.item(i, tags)) for i in items]

	@jsonify
	def groups(self, username, itemtype):
		try:
			(c.user, itemtype, stype, count, offset, tags) = \
					self._get_params(username, itemtype)
		except ItemsControllerException, e:
			abort(404, e.message)
		# query
		q = ItemGroup.query.join(['account', 'service', 'type']) \
			.filter(Account.user_id  == c.user.id) \
			.filter(ServiceType.type == stype)
		itemgroups = q[offset:offset + count].all()
		groups = [dict(self.itemgroup(i)) for i in itemgroups]
		return {'user': username, 'type': itemtype, 'count': count, \
				'offset': offset, 'groups': groups}

	def _get_params(self, username, itemtype):
		# Validate item type and user existence
		stype = self._translate_servicetype(itemtype)
		itemtype = self._translate_itemtype(itemtype)
		if itemtype is None:
			raise ItemsControllerException, 'No such item type'
		user = User.get_by(username=username)
		if user is None:
			raise ItemsControllerException, 'No such user'
		# GET parameters
		count = min(100, self._get_int_param('count', 20))
		offset = self._get_int_param('offset', 0)
		tags = self._get_int_param('tags', 0)
		return (user, itemtype, stype, count, offset, tags)

	def _get_int_param(self, key, default=0):
		try:
			return int(request.params.get(key, default))
		except:
			return default

	def _translate_itemtype(self, itemtype):
		d = {'videos': 'video', 'pictures': 'photo', \
				'bookmarks': 'bookmark', 'music': 'music', \
				'artists': 'music', 'songs': 'music', \
				'quotes': 'quote', 'blogs': 'article'}
		return d.get(itemtype)

	def _translate_servicetype(self, itemtype):
		no_trans = ['videos', 'pictures', 'bookmarks', 'music', \
				'quotes', 'blogs']
		d = {'artists': 'music', 'songs': 'music'}
		return itemtype if itemtype in no_trans else d.get(itemtype)

	def _itemtodict(self, item, mapping, d={}):
		"""
		Returns a dictionary with the item's attributes according
		to the mapping, that has the item attribute names as keys and
		the new dictionary keys as its values. The value of the
		inexistent attributes in the new dictionary will be None.
		"""
		for i in mapping:
			d[mapping[i]] = getattr(item, i, None)
		return d

	def _attrmap(self, attrs):
		"""Converts [a, b, ...] to {a: a, b: b, ...}"""
		return dict([(i, i) for i in attrs])

	def item(self, useritem, tags=0):
		"""Returns a dictionary with the item's attributes"""
		date = useritem.creation_date
		attrs = ['id', 'external_id', 'service', 'title', \
				'description'] # TODO: include import_date?
		mapping = self._attrmap(attrs)
		mapping.update({'row_type': 'type'})
		d = self.item_with_tags(useritem, tags) if tags > 0 else {}
		self._itemtodict(useritem.item, mapping, d)
		# post-itemtodict conversions (mostly to be able to jsonify)
		d['date'] = '%s' % date
		#d['import_date'] = '%s' % d['import_date']
		d['service'] = '%s' % getattr(d['service'], 'name', None)
		return d

	def item_with_tags(self, useritem, tagscount):
		"""Returns a dictionary with a single key 'tags' whose value
		is an array of the item's tags (strings)"""
		tags = useritem.tags[0:tagscount]
		# No distinction between useritem tags and item tags here.
		# Both kinds are found in useritems.tags 
		return {'tags': [i.name for i in tags]}

	def itemgroup(self, itemgroup):
		attrs = ['id', 'import_date', 'name', 'description', \
				'external_id', 'is_null_group', 'account']
		d = self._itemtodict(itemgroup, self._attrmap(attrs))
		# post-itemtodict conversions
		# TODO: eagerload de account y service
		d['import_date'] = '%s' % d['import_date']
		d['account'] = {'username': d['account'].username, \
				'service': d['account'].service.name}
		return d

	def video(self, useritem, d={}):
		mapping = {'embedURL': 'url', 'externalURL': 'external_url', \
				'thumbnails': 'thumbnails'}
		d = self._itemtodict(useritem.item, mapping, d)
		# post-itemtodict conversions
		d['thumbnails'] = [i.url for i in d['thumbnails']]
		# TODO: quizas se quiera exponer width, height y time de thumbs
		return d

	def photo(self, useritem, d={}):
		mapping = {'url': 'url', 'external_url': 'external_url', \
				'thumbnail_url': 'thumbnail'}
		return self._itemtodict(useritem.item, mapping, d)

	def bookmark(self, useritem, d={}):
		mapping = {'url': 'url', 'serviceUrl': 'external_url', \
				'popularity': 'popularity'}
		return self._itemtodict(useritem.item, mapping, d)

	def music(self, useritem, d={}):
		if useritem.row_type == 'songuseritem':
			return self.song(useritem, d)
		elif useritem.row_type == 'artistuseritem':
			return self.artist(useritem, d)
		return d
	
	def song(self, useritem, d={}):
		d['playcount'] = getattr(useritem, 'play_count', None)
		d['external_url'] = getattr(useritem.item, 'external_id', None)
		artist = useritem.item.artist
		d['artist'] = {'name': artist.title, \
				'thumbnail': artist.photo_url, \
				'external_id': artist.external_id, \
				'id': artist.id}
		return d

	def artist(self, useritem, d={}):
		d['playcount'] = getattr(useritem, 'play_count', None)
		d['thumbnail'] = getattr(useritem.item, 'photo_url', None)
		return d

	def quote(self, useritem, d={}):
		attrs = ['external_url', 'publish_date']
		d = self._itemtodict(useritem.item, self._attrmap(attrs), d)
		# post-itemtodict conversions
		d['publish_date'] = '%s' % d['publish_date']
		return d

	def article(self, useritem, d={}):
		attrs = ['external_url', 'publish_date']
		d = self._itemtodict(useritem.item, self._attrmap(attrs), d)
		# post-itemtodict conversions
		d['publish_date'] = '%s' % d['publish_date']
		return d



class ItemsControllerException(Exception):
	pass

