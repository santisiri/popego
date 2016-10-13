# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from formencode import Schema
import popserver.validators as v
from datetime import datetime
#from popserver.model import Country

from popserver.model import User

usernameValidator = v.Regex(r'^[a-zA-Z0-9_.-]+$', not_empty=True, strip=True)
passwordValidator = v.String(not_empty=True)

class BaseUserRegistration(Schema):
  username           = v.Chain(v.UniqueCaseInsensitive(User, 'username'), \
		                usernameValidator)
  password           = passwordValidator
  password_confirm   = passwordValidator
  chained_validators = [v.FieldsMatch('password','password_confirm')]

class UserRegistration(BaseUserRegistration):
  displayname        = v.UnicodeString(not_empty=True, strip=True)
  email              = v.Chain(v.Email(not_empty=True), v.Unique(User,'email'))
  shortBio           = v.String(max=250,not_empty=False)

class UserAlphaRegistration(BaseUserRegistration):
  activation_code    = v.Regex(r'^[a-f0-9]{32}$', not_empty=True, strip=True)
  terms_of_use       = v.OneOf(['agree'])

class UserLogin(Schema):
  username           = usernameValidator
  password           = passwordValidator

class UserPersonalSettings(Schema):
	fullname  = v.UnicodeString(not_empty=True, strip=True)
	website   = v.URL(add_http=True)
	email     = v.Chain(v.Email(not_empty=True), v.Unique(User,'email'))
	minibio   = v.UnicodeString(max=250)
	birthdate = v.DateConverter(not_empty=False)
	gender    = v.OneOf(['M', 'F', None])
	country   = v.Regex(r'^([a-z]{2}|--)$', strip=True)
	# Podria ser: v.OneOf([i.id for i in Country.query.all()])
	# Pero eso podria generar:
	# sqlalchemy.exceptions.InvalidRequestError: Could not locate any
	# Engine or Connection bound to mapper 'Mapper|Country|countries'

class UserPasswordSettings(Schema):
	current_password   = v.String(not_empty=True)
	new_password       = v.String(min=4, not_empty=True)
	confirm_password   = v.String(min=4, not_empty=True)
	chained_validators = [v.FieldsMatch('new_password','confirm_password')]

#class UserPopegoSettings(Schema):
#	recognize_popego   = v.OneOf(['always', 'signup', 'never'])
#	contactable_by     = v.OneOf(['anyone', 'users', 'poplist'])
#	third_party_access = v.OneOf(['all', 'personal', 'tags', 'nothing'])

