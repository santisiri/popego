# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import logging, formencode

from popserver.lib.base import *
from popserver.model import TagCount
import elixir
from sqlalchemy import text
from sqlalchemy.orm import eagerload
import os.path
from datetime import datetime
from routes import url_for
from popserver.ai import compatibility

from urllib import urlopen
import simplejson
import re

log = logging.getLogger(__name__)

class UsersController(BaseController):

  def index(self):

	if self._isUserAuthenticated():
		return redirect_to(action='home', username=self.user.username)

	# Esto es para alpha signup
	if config.get('popego.allow_alpha_signups', False):
		return self._alpha_index()

	# Esto es para el verdadero signup
	if len(request.POST) > 0:
		try:
			schema = forms.UserRegistration()
			form_result = schema.to_python(request.POST)

			u = model.User(**form_result)
			model.dbsession.flush()

			self._login(u.username)
			return redirect_to(action='home', username=u.username)
        
		except formencode.Invalid, error:
			c.form_result = error.value
			c.form_errors = error.error_dict or {}

	return render('/website/home/registration.mako')


  @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
  def home(self):
	c.user = self.user
	c.lastPopegos = []

	conn = elixir.metadata.bind.connect()
	s = text('SELECT u.id, w.template, w.theme, ' \
			'w.best_referrer FROM widgets w JOIN users u ' \
			'ON w.user_id = u.id ' \
            'WHERE w.best_referrer IS NOT NULL ORDER BY random() LIMIT 8')
	ws = conn.execute(s).fetchall()

	for w in ws:
		u = model.User.query.filter_by(id = w[0]).first()
		compat = compatibility.compatibilityFor(self.user, u)
		c.lastPopegos.append({'template': w[1], 'theme': w[2], \
			'url': w[3], 'user': u, 'compatibility': compat})
	
	return render('/website/user/home.mako')

  def _alpha_index(self):

	if 'activation_code' in request.POST:
		h = request.POST['activation_code']
	else:
		h = request.params.get('h', '')

	info = self._get_alpha_tester_info(h)
	if info is None:
		return redirect_to(controller='website/home')

	if len(request.POST) > 0:
		try:
			schema = forms.UserAlphaRegistration()
			form_result = schema.to_python(request.POST)
			d = {'shortBio': '', 'displayname': info['name'], \
				'email': info['email'], 'website': info['url']}
			form_result.update(d)

			u = model.User(**form_result)
			model.dbsession.flush()
			self._activate_alpha_tester(h)

			self._login(u.username)
			return redirect_to(controller='website/service', \
					action='index', username=u.username)

		except formencode.Invalid, error:
			c.form_result = error.value
			c.form_errors = error.error_dict or {}
		except:
			# User(**form_result) puede fallar por email duplicado
			c.form_errors = {'username': 'Cannot create user. ' \
					'Maybe you already signed up.'}

	c.fullName = info.get('name', '')
	c.activationCode = h
	return render('/website/home/alpha_registration.mako')

  def _get_alpha_tester_info(self, h):
	externalServiceUrl = 'http://www.popego.com/admin/query.php'
	info = None
	try:
		if re.match('^[0-9a-f]{32}$', h):
			u = urlopen('%s?h=%s' % (externalServiceUrl, h))
			info = simplejson.loads(u.read()) or None
  			# Esto convierte los strings de la info del 
			# alpha tester que quedaron con mal escapados 
			# un encoding del tipo 'xmlcharrefreplace'.
			if info is not None:
				for i in info:
					info[i] = self._unescape(info[i])
	except:
		pass
	
	return info

  def _activate_alpha_tester(self, h):
	externalServiceUrl = 'http://www.popego.com/admin/query.php'
	try:
		u = urlopen('%s?h=%s&activated=1' % (externalServiceUrl, h))
	except:
		pass

  def _unescape(self, s):
	return re.sub('&#(\d+);', lambda (x): unichr(eval(x.group(1))), s)

