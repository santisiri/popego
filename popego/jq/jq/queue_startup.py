from twisted.application import internet, service, strports
from jq.queue.producerend import QueueFactory
from twisted.web2 import server, channel
from jq.queue.error_rss import ErrorRssResource
from jq.queue.consumerend import TwistedJobConsumer
from jq.queue.model import JobScheduler
from jq.queue import dbclasses

def createQueue(port=8787, name=None, app=None, consumers=[], timerStep=1000,
                withRss=False, rssPort=6666):
    assert name is not None
    assert app is not None
    assert len(consumers) > 0

    queueModel = __getQueue(name) 
    scheduler = JobScheduler(queueModel)

    for chost, cport in consumers:
        scheduler.addConsumer(TwistedJobConsumer(chost, cport))



    queue =  internet.TCPServer(port, QueueFactory(scheduler))
    queue.setServiceParent(app)    
    timer = internet.TimerService(timerStep, scheduler.dispatchPending)
    timer.setServiceParent(app)

    if (withRss):
        site = server.Site(ErrorRssResource())
        rss = strports.service('tcp:%s' % str(rssPort), channel.HTTPFactory(site))
        rss.setServiceParent(app)


def __getQueue(queueName):
    session = dbclasses.Session()
    queue = session.query(dbclasses.Queue).get_by(name=queueName)
    if not queue:
        queue = dbclasses.Queue(queueName)
        session.save(queue)
        session.commit()
    return queue
    
