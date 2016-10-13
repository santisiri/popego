from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapper, sessionmaker, relation, scoped_session

from datetime import datetime

# Model Classes
class Queue(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Queue: %s>" % self.name

class Job(object):
    def __init__(self, priority, type, data=None):
        self.priority = priority
        self.type = type
        self.data = data
        self.creation_date = datetime.now()

    def __repr__(self):
        return "<Job(%s - [%s#%s])>" % (self.type, self.priority, self.creation_date)

# To be populated on dbInit() call
engine = None
metadata = None
Session = None
tables = {}

def dbInit(connstr):
    me = __import__(__name__, fromlist='__name__')
    me.engine = create_engine(connstr)
    me.metadata = MetaData()
    me.metadata.bind = me.engine
    me.Session = scoped_session(sessionmaker(bind=me.engine, autoflush=True, 
                                    transactional=True))
    tables['jobs'] = Table('jobs', me.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('queue_id',None, 
                                  ForeignKey('queues.id'),
                                  nullable=False),
                           Column('type',Text, nullable=False),
                           Column('data',Text),
                           Column('priority',Integer),
                           Column('creation_date',DateTime, 
                                  nullable=False),
                           Column('started_date', DateTime),
                           Column('ended_date', DateTime),
                           Column('error',Text))
    tables['queues'] = Table('queues', me.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name',Text, nullable=False))
                             
    mapper(Job, tables['jobs'])
    mapper(Queue, tables['queues'],
           properties={'jobs':relation(Job, backref='queue')})
