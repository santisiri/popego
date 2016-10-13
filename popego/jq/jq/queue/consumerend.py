from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, error
from twisted.python import log
from jq.common import VariablePacketProtocol
import pickle, types
import functools

class ConsumerClientProtocol(VariablePacketProtocol):
    def connectionMade(self):
        data = pickle.dumps((self.factory.job.type, self.factory.job.data))
        self.sendPacket(data)

    def packetRecieved(self, packetData):
        error = pickle.loads(packetData)
        if error is not None and len(error.strip()) == 0:
            error = None
        self.factory.jobDone(error)
        self.transport.loseConnection()

class ConsumerClientFactory(ClientFactory):
    protocol = ConsumerClientProtocol

    def __init__(self, job, callback):
        self.job = job
        self.callback = callback

    def jobDone(self, error):
        self.callback(error)

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection.  Reason: %s' % reason)

    def clientConnectionFailed(self, connector, reason):
        log.msg('Connection failed.  Reason: %s' % reason)

class JobConsumer(object):
    def performJob(job, onFinishClbk):
        """Performs the given Job, and call the onFinishCallback"""
        raise NotImplementedError, "Dummy Implementation"

class TwistedJobConsumer(JobConsumer):
    def __init__(self, host, port):
        assert isinstance(port, types.IntType)
        self.host = host
        self.port = port

    def performJob(self, job, onFinishClbk):
        callback = functools.partial(onFinishClbk, self, job)
        clientFactory = ConsumerClientFactory(job, callback)
        reactor.connectTCP(self.host, self.port, clientFactory)
        
    def __repr__(self):
        return "<TwistedJobConsumer(host=%s, port=%s)>" % (self.host, self.port)
