"""\
Paster create template for creating your own authentication methods.
"""
from paste.script.templates import BasicPackage

class AuthenticatePlugin(BasicPackage):
    _template_dir = 'authenticate'
    summary = "An AuthKit authenticate middleware plugin"

