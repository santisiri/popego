from sqlalchemy.orm import mapper
from datetime import datetime
from dbclasses import *
from twisted.python import log
import types

class JobScheduler(object):
    def __init__(self, queue):
        self.session = Session()
        self.queue = queue
        self.consumers = set()
        self.idleConsumers = set()

    def addJob(self, priority, type, data):
        """Adds a new Job to the JobQueue"""
        assert isinstance(priority, types.IntType)
        job = Job(priority, type,data)
        job.queue = self.queue
        log.msg("AddJob: queue: %s job: %s" % (self.queue, job))
        self.session.save(job)
        self.session.commit()
        self.dispatchPending()
        
    def dispatchPending(self):
        """Dispatchs Pending Jobs to Idle JobConsumers"""
        pendingJobs = self._getPendingJobs()
        
        while len(self.idleConsumers) > 0 and len(pendingJobs) >0:
            consumer = self.idleConsumers.pop()
            job = pendingJobs.pop(0)
            job.started_date = datetime.now()
            log.msg("Job %s assigned to consumer %s" % (job, consumer))
            consumer.performJob(job, self._jobFinished)
        
        self.session.commit()

    def _getPendingJobs(self):
        jobs = self.session.query(Job).filter(Job.started_date==None) \
            .filter(Job.queue == self.queue) \
            .order_by([Job.priority.asc(), Job.creation_date.asc()]).all()
        return jobs
        

    def addConsumer(self, jobConsumer):
        """Adds a JobConsumer to the JobScheduler"""
        self.consumers.add(jobConsumer)
        self.idleConsumers.add(jobConsumer)

    def _jobFinished(self, consumer, job, error):
        """Event listener, to deal with finished jobs"""
        job.ended_date = datetime.now()
        job.error = error
        log.msg("Job %s finished" % job)
        self.idleConsumers.add(consumer)
        self.session.commit()
        self.dispatchPending()
