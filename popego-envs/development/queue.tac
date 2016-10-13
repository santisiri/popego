# EXAMPLE queue.tac
# - se asocia con el job consumer que corre en puerto 9000
# - crea el servicio de Queue en puerto 8787
# - Setea un periodo de 1000msec para el despacho de trabajos pendientes
from jq.queue.dbclasses import dbInit
dbInit("postgres://popego:GranPopego@localhost:5432/PopegoQueue")

from jq.queue_startup import createQueue
from twisted.application.service import Application
application = Application("JobQueue Application")
createQueue(port=8787, 
            name='NewAccounts', 
            app= application,
            consumers= [('localhost', 9000)]
            )

createQueue(port=8788, 
            name='AccountUpdates', 
            app= application,
            consumers= [('localhost', 9001)]
            )
