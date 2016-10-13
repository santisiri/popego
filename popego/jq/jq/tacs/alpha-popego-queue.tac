# - asocia con los job consumers
# - crea el servicio de Queue en puerto 8787
# - Setea un periodo de 1000msec para el despacho de trabajos pendientes

from jq.queue.dbsetup import DBSetup

DBSetup().setup("postgres://popego:GranPopego@popego-db:5432/popego_alpha_queue")


from jq.queue.consumerend import TwistedJobConsumer
from jq.queue_startup import *

from jq.queue.model import JobScheduler
jobScheduler = JobScheduler()

for i in range(0,4):
    jobScheduler.addConsumer(TwistedJobConsumer('localhost',9000 + i))

attachProducersService(8787, application, jobScheduler)
attachConsumersService(1000, application, jobScheduler)
attachErrorRssService(6666, application)