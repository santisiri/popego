from twisted.internet.protocol import Protocol

class VariablePacketProtocol(Protocol):

    def __init__(self):
        self.buffer = ""
        self.inHeader = True
        self.headerLen = 10


    def _canProcess(self):
        return self._canProcessHeader() or self._canProcessBody()

    def _canProcessHeader(self):
        return self.inHeader and len(self.buffer) >= self.headerLen

    def _canProcessBody(self):
        return not self.inHeader and len(self.buffer) >= self.bodyLen

    def dataReceived(self, data):
        self.buffer += data

        while self._canProcess():
            if self._canProcessHeader():
                self.inHeader = False
                self.bodyLen = int(self.buffer[0:self.headerLen])
                self.buffer = self.buffer[self.headerLen:]

            if self._canProcessBody():
                    packetData = self.buffer[0:self.bodyLen]
                    self.buffer = self.buffer[self.bodyLen:]
                    self.inHeader = True
                    self.packetRecieved(packetData)

    def sendPacket(self, packetData):
        dataLen = len(packetData)
        if (dataLen > 9999999999):
            raise error
    
        packet = "%010d%s" % (dataLen,packetData)
        self.transport.write(packet)
