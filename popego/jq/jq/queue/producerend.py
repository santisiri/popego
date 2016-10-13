from twisted.internet import protocol
from jq.common import VariablePacketProtocol
import pickle

class QueueProtocol(VariablePacketProtocol):
    def packetRecieved(self, packetData):
        priority, type, data = pickle.loads(packetData)
        self.factory.newJob(priority, type, data)

class QueueFactory(protocol.ServerFactory):
    protocol = QueueProtocol

    def __init__(self, jobScheduler):
        self.jobScheduler = jobScheduler

    def newJob(self, priority, jobType, data):
        self.jobScheduler.addJob(priority, jobType, data)

