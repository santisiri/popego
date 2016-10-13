from twisted.internet import protocol
from jq.common import VariablePacketProtocol
import pickle, traceback
from twisted.python import log
from twisted.internet import utils
import os


class JobConsumerProtocol(VariablePacketProtocol):

    def packetRecieved(self, packetData):

        def cb(output):
            """ Callback para el deferred """
            log.msg(output)
            firstAndRest = output.split('\n',1)
            
            if firstAndRest[0] == 'FinishedWithError' or len(firstAndRest) > 1:
                self.sendPacket(pickle.dumps(firstAndRest[1]))
            else:
                self.sendPacket(pickle.dumps(None))
            
        def eb(failure):
            """ Errback para el deferred """
            log.msg('job `%s - %s` finished with unexpected error' \
                        % (type, data))
            tb = failure.getTraceback(elideFrameworkCode=1)
            log.msg(tb)
            self.sendPacket(pickle.dumps(tb))
 
        type, data = pickle.loads(packetData)

        deferred = self.factory.dispatchJob(type, data)
        deferred.addCallbacks(cb, eb)

class JobConsumerFactory(protocol.ServerFactory):
    protocol = JobConsumerProtocol

    def __init__(self, consumerExecutable):
        self.consumerExecutable = consumerExecutable

    def dispatchJob(self, type, data):
        log.msg("Dispatching Job (asynchronously): %s - %s" % (type, data))
        return utils.getProcessOutput('python', 
                                      args=[self.consumerExecutable, str(type),
                                            str(data)], 
                                      env=os.environ,
                                      errortoo=1)
    
