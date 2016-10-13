from popserver.lib.base import *
import logging
import os
import formencode
from datetime import datetime
from time import strptime, mktime
from popserver.model import Country
from routes import url_for
import re

try:
	import Image
except:
	from PIL import Image


log = logging.getLogger(__name__)


class SettingsController(BaseController):

	@authorize(And(UserInRoute('username'),ValidAuthKitUser()))    
	def index(self):
		c.user = self.user
		c.myAvatar = h.url_for_user_avatar(c.user, 200, force=True)
		countries = Country.query.all()
		c.countries = [(i.id, i.name) for i in countries]
		c.countries.sort(cmp=lambda x,y: -1 if y[0] == '--' \
				else cmp(x[1], y[1]))
		return render('/website/user/settings.mako')


	@authorize(And(UserInRoute('username'),ValidAuthKitUser()))    
	@jsonify
	def personal_settings(self):
		schema = forms.UserPersonalSettings()
		user = self.user
		reserved_email = 'secret.inexistent.address@popego.com'

		try:
			# birthyear, birthmonth, birthday (strings) -> 
			# t (string)
			d = request.POST
			t = '%s/%s/%s' % (d['birthmonth'].strip(), \
				d['birthday'].strip(), d['birthyear'].strip())
			del d['birthyear']
			del d['birthmonth']
			del d['birthday']
			d['birthdate'] = ('' if t == '//' else t)

			# FIXME: esto es un hack trucho para que el email 
			# no parezca ya existente por culpa del mismo usuario
			if d['email'] == user.email:
				d['email'] = reserved_email

			# gender is expected but can be null
			if 'gender' not in d:
				d['gender'] = None

			# formencode validation/conversion
			result = schema.to_python(d)

			# country might violate foreign key
			if Country.query.filter_by(id=result['country']) \
					.count() < 1:
				result['country'] = None
	
			# persistance
			user.displayname = result['fullname']
			if result['email'] != reserved_email:
				user.email = result['email']
			else:
				result['email'] = user.email
			user.website = result['website'] or ''
			user.gender = result['gender']
			user.birthdate = result['birthdate']
			user.country_id = result['country']
			user.shortBio = result['minibio'] or ''
			user.flush()

			# t (datetime) ->
			# birthyear, birthmonth, birthday (strings)
			t = result['birthdate']
			result['birthyear'] = '%d' % t.year if t else ''
			result['birthmonth'] = '%d' % t.month if t else ''
			result['birthday'] = '%d' % t.day if t else ''
			del result['birthdate']

		except formencode.Invalid, e:
			result = '%s' % e
			hardcoded_msg = 'birthdate: Please enter a valid date'
			p = re.compile(r'\bbirthdate: [\w ]*mm/dd/yyyy\b')
			result = p.sub(hardcoded_msg, result)
		except Exception, e:
			result = 'Yikes! Cannot update your profile. '\
					'Try again later...'
# 		        result = '%s' % e # this is too much information

		return result


	@authorize(And(UserInRoute('username'),ValidAuthKitUser()))    
	@jsonify
	def password_settings(self):
		schema = forms.UserPasswordSettings()
		user = self.user
		msg = ''

		try:
			# formencode validation/conversion
			r = schema.to_python(request.POST)

			# persistance
			if not user.changePassword(r['current_password'], \
				r['new_password'], r['confirm_password']):
				raise Exception
			user.flush()

		except formencode.Invalid, e:
			msg = '%s' % e
		except Exception:
			msg = 'Uh-oh! Failed to change your password. ' \
					'Try again...'

		return msg


	@authorize(And(UserInRoute('username'),ValidAuthKitUser()))    
	def upload(self, username):
		user = self.user

		if 'my_avatar' not in request.POST:
			return 'No file uploaded'

		try:
			my_avatar = request.POST['my_avatar']
			self._saveAvatars(my_avatar.file, user.username)
			my_avatar.file.close()
			user.avatar_mtime = datetime.now()
			user.flush()
		except Exception, e:
    			return 'Yikes! Cannot upload this file as your avatar'
			#return '%s' % e # this is too much information
    
        	return ''


	def _convertToAvatar(self, infile, convert = 'RGB'):
		im = Image.open(infile)
		# By default, convert to RGB (if not already RGB)
		if convert and im.mode != convert:
			im.draft(convert, im.size)
			im = im.convert(convert)
		# Crop to max centered square
		minxy = min(*im.size)
		left = (im.size[0] - minxy) / 2
		upper = (im.size[1] - minxy) / 2
		box = (left, upper, left + minxy, upper + minxy)
		im = im.crop(box)
		return im


	def _saveAvatars(self, infile, username):
		# infile/outfile can be an open file or a filename string
		options = {}
		im = self._convertToAvatar(infile)
		sizes = self._getAvailableSizesForAvatar()
		# Save avatar copies in given sizes in JPEG format
		for i in sizes:
			size = (i, i)
			outfile = self._path_for_avatar(username, i)
			resized_image = im.resize(size, Image.ANTIALIAS)
			resized_image.load()
			apply(resized_image.save, (outfile, 'JPEG'), options)

	def _getAvailableSizesForAvatar(self):
		return [50, 75, 100, 125, 150, 175, 200]

	def _getBestAvailableSizeForAvatar(self, size=200):
		sizes = self._getAvailableSizesForAvatar()
		try:
			sizes = [50, 75, 100, 125, 150, 175, 200]
			size = int(size)
			for i in sizes:
				if i >= size:
					size = i
					break
			else:
				size = sizes[-1]
		except Exception:
			size = sizes[-1]

		return size

	def _path_for_avatar(self, username, size):
		return os.path.join(config['pylons.paths']['static_files'], \
				'upload/user_avatars', \
				'%s.%d.jpg' % (username, size))
