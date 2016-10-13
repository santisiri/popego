import re
import libgmail

class Contact(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Contact: %s - %s>' % (self.name, self.email)


class BadLogin(Exception):
    pass

class AddressBookAccount(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._logged = False

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._username)

    def login(self):
        raise NotImplementedError()

    def get_all_contacts(self):
        raise NotImplementedError()


class GoogleAddressBookAccount(AddressBookAccount):
    def __init__(self, username, password):
        super(GoogleAddressBookAccount, self).__init__(username, password)
        self._acc = libgmail.GmailAccount(self._username, self._password)

    def login(self):
        if not self._logged:
            try:
                self._acc.login()
                self._logged = True
            except Exception, e:
                raise BadLogin('Google')

    def get_all_contacts(self):
        self.login()
        d = self._acc.getContacts()
        return [Contact(x.name, x.email) for x in d.getAllContacts()]


class AddressBookAccountsManager(object):
    _re_mails = (
        (r'^.*@(gmail|google)\.com$', GoogleAddressBookAccount), )

    @classmethod
    def get_account_for(cls, username, password):
        for k,v in cls._re_mails:
            if re.match(k, username):
                return v(username, password)
        raise ValueError("Couldn't determine provider for %s" % username)



