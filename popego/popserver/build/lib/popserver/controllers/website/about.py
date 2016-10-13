import logging

import os
import shutil
import cgi
from datetime import datetime
from smtplib import SMTPException
from popserver.lib.base import *
from popserver.model import Feedback
from popserver.lib.mailer import Mailer

log = logging.getLogger(__name__)

try:
	import Image
except:
	from PIL import Image


class AboutController(BaseController):

	def index(self):
		self.tos()

	def tos(self):
		return render('/website/about/tos.mako')

	def developers(self):
		return render('/website/about/developers.mako')

	@authorize(And(UserInRoute('username'),ValidAuthKitUser()))
	def user_feedback(self):
		return self.feedback()

	def feedback(self):
		c.user = self.user or None
		if request.POST:
			c.result = self.submit_feedback()
			return render('website/about/feedback.mako')
		else:
			c.result = None
			return render('website/about/feedback.mako')

	def submit_feedback(self):
		report = request.POST.get('report', '')
		description = request.POST.get('desc', '')
		if not description:
			return 'Please enter a message'

		try:
			t = datetime.now()
			agent = request.environ['HTTP_USER_AGENT']
			f = Feedback(user = self.user or None, \
				type = report, comment = description, \
				user_agent = agent, creation_date = t)
			f.flush()
		except Exception, e:
			# return 'Feedback submission error: %s' % e
			return 'Failed to submit feedback'

		try:
			self._sendmail(f)
		except:
			pass

		try:
			s = request.POST['screenshot']
			if isinstance(s, cgi.FieldStorage):
				self._saveScreenshot(s.file, f.id)
		except Exception, e:
			# return 'Screenshot upload error: %s' % e
			return 'Feedback was sent but screenshot upload failed'

		return ''

	def _saveScreenshot(self, infile, id):
		# some params...
		options = {}
		convert = 'RGB'
		maxsize = (800, 600)
		accepted_formats = ['JPEG', 'GIF', 'PNG']
		outfile_path = self._path_for_screenshot(id)
		# If image has an accepted format and is smaller than maxsize
		# (in both width and height), move file
		# Else convert to JPEG (in RGB and not so big)
		im = Image.open(infile)
		if im.format in accepted_formats and im.size[0] < maxsize[0] \
				and im.size[1] < maxsize[1]:
        		outfile = open(outfile_path, 'w') # string to file
			infile.seek(0)
			shutil.copyfileobj(infile, outfile, -1)
			infile.close()
			outfile.close()
		else:
			if convert and im.mode != convert:
				im.draft(convert, im.size)
				im = im.convert(convert)
			# Resize (if too big) and save
			im = self._resizeScreenshot(im, maxsize)
			im.load()
			apply(im.save, (outfile_path, 'JPEG'), options)
			infile.close()

	def _resizeScreenshot(self, im, maxsize):
		(w, h) = im.size
		if w > maxsize[0]:
			h = maxsize[0] * h / w
			w = maxsize[0] # * w / w
		if h > maxsize[1]:
			w = maxsize[1] * w / h
			h = maxsize[1] # * h / h
		newsize = (w, h)
		if im.size != newsize:
			im = im.resize(newsize, Image.ANTIALIAS)
		return im
	
	def _path_for_screenshot(self, id):
		basepath = config['pylons.paths']['static_files']
		return os.path.join(basepath, 'upload/feedback', '%d.jpg' % id)

	def _sendmail(self, f):
		u = f.user.username if f.user else 'An anonymous user'
		fromaddr = 'Popego Feedback <feedback@popego.com>'
		toaddrs = ['Popego Feedback <feedback@popego.com>']
		action = {'bug': 'reported a bug', \
			'suggest': 'suggested an idea', \
			'contact': 'wants to contact the team'} \
			.get(f.type, 'sent some comments')
		subject = 'Popego Feedback: %s %s!' % (u, action)
		msg = 'Popego user "%s" %s!\nFeedback was sent on %s with ' \
			'the following HTTP_USER_AGENT data:\n%s\n\n%s' \
			% (u, action, f.creation_date, f.user_agent, f.comment)
		m = Mailer()
		m.sendmail(fromaddr, toaddrs, subject, msg)
		return f

