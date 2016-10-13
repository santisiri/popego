# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from pylons import config
import smtplib

class Mailer(object):

    def __init__(self):
        self.host = config.get('popego.smtp.host', 'localhost')
        self.port = config.get('popego.smtp.port', 25)
        self.auth = config.get('popego.smtp.auth', False)
        self.username = config.get('popego.smtp.username', '')
        self.password = config.get('popego.smtp.password', '')

    def sendmail(self, fromaddr, toaddrs, subject, msg):
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" \
		    % (fromaddr, ", ".join(toaddrs), subject, msg)

        session = smtplib.SMTP(self.host, self.port)
        session.ehlo()
        if self.auth:
            session.starttls()
            session.ehlo()
            session.esmtp_features['auth'] = 'LOGIN PLAIN'
            session.login(self.username, self.password)

        result = session.sendmail(fromaddr, toaddrs, msg)
        session.quit()
	return result

