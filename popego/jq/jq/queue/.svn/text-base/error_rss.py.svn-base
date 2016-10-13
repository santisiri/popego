# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from twisted.web2 import resource, http
from jq.queue.model import Job
from jq.queue import dbclasses
from popserver.lib.atomgenerator import AtomFeed
from datetime import datetime

class ErrorRssResource(resource.Resource):
    addSlash = True
    def render(self, ctx):
        session = dbclasses.Session()
        jobs = session.query(Job).filter(Job.error!=None) \
            .order_by(Job.started_date.desc())[0:20].all()


        feed = AtomFeed("errores-queue","Errores Agentes", datetime.utcnow())
        for job in jobs:
            id = job.id
            title = "On %s, error en Job %s - Account %s" % (job.creation_date,
                                                             job.type, job.data)
            summary = job.error
            feed.addEntry(id, title, job.started_date, summary)
        
        return http.Response(stream=feed.toString())

#jobs = self.session.query(Job).filter(Job.started_date==None) \
#    .order_by(Job.creation_date.asc()).all()
