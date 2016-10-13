
from popserver.model import *
from popserver.lib import jq_client 
from popserver.cron import config

# TODO: puede pasar que halla un update ya encolado, y lo vuelva a poner en cola
# TODO: puede pasar que halla un update corriendo y no se da cuenta

__jobDescription__ = """
Actualiza los datos de todos los accounts
"""


def start(hostname=None, port=None):
    queue = (hostname or config['jqueue.hostname'], 
             int(port or config['jqueue.port']))

    for a in Account.query.all():
        jq_client.newJob("updateAccount", a.id,
                         queue[0], queue[1])
