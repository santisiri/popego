from twisted.internet import protocol
from jq.common import VariablePacketProtocol
import pickle

class ControlProtocol(VariablePacketProtocol):
    def packetRecieved(self, packetData):
        mType, srvAddr = pickle.loads(packetData)
        
        if mType == 'newConsumer':
            self.factory.newConsumer(mType)
        elif mType == 'jobFinished':
            self.factory.consumerIdle(srvAddr)

class ControlServerFactory(protocol.ServerFactory):
    protocol = ControlProtocol

    def __init__(self, consumersPool):
        self.consumersPool = consumersPool

    def newConsumer(self, srvAddr):
        self.consumersPool.registerServer(srvAddr)
    def consumerIdle(self, srvAddr):
        self.consumersPool.markSrvIdle(srvAddr)
