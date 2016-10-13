# - asocia con los job consumers
# - crea el servicio de Queue en puerto 8787
# - Setea un periodo de 1000msec para el despacho de trabajos pendientes
from jq.queue.dbclasses import dbInit
dbInit("postgres://popego:GranPopego@popego-db:5432/popego_alpha_queue")


from jq.queue_startup import createQueue
from twisted.application.service import Application
application = Application("JobQueue Application")
createQueue(port=8787, 
            name='NewAccounts', 
            app= application,
            consumers= [('localhost', 9000),
                        ('localhost', 9001),
                        ('localhost', 9002),
                        ('localhost', 9003),
                        ]
            )

createQueue(port=8788, 
            name='AccountUpdates', 
            app= application,
            consumers= [('localhost', 9004),
                        ('localhost', 9005)
                        ]
            )
