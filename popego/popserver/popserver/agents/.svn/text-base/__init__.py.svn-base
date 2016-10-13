# -*- coding: utf-8 -*-
# inicializa atributos de los módulos con las tuplas definidas en agents.ini
#
# Ejemplo:
#
# [flickr_agent]
# host = http://flickr.com
# api_endpoint = /services/rest
# api_key = 3688e2ed7d18224b4d2c877c5541f89d
#
# Ejecuta:
#
# import agents.flickr_agent
# agents.flickr_agent.host = 'http://flickr.com'
# agents.flicrk_agent.api_endpoint = '_agent.host = 'http://flickr.com''
# agents.flickr_agent.api_key = '3688e2ed7d18224b4d2c877c5541f89d'
from __future__ import with_statement
import ConfigParser, os


confFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agents.ini')
cfgp = ConfigParser.ConfigParser()
with open(confFilePath) as file:
    cfgp.readfp(file)

for module_name in cfgp.sections():
    mod = __import__('popserver.agents', globals(), locals(), [module_name], -1)
    mod = getattr(mod, module_name)
    for prop in cfgp.items(module_name):
        setattr(mod, prop[0], prop[1])

# excepciones

class AgentException(Exception): 
    """ clase base para todas las Exceptions emitidas por los agentes """
    pass

class ItemNotFoundException(AgentException): 
    """ el item solicitado no pudo ser encontrado por el agente en el servicio remoto """
    pass


