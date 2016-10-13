import pickle
import socket

class QueueClient(object):
    def __init__(self, host, port):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host,port))
        except socket.error, e:
            print "Connection Error: %s" % e
        

    def enqueueJob(self, type,data):
        packet = self._createPacket((type,data))

        try:
            self.s.send(packet)
        except socket.error, e:
            print "Error sending data: %s" % e

    def _createPacket(self, data):
        rawData = pickle.dumps(data)
        lenData = len(rawData)
        return "%010d%s" % (lenData, rawData)

    def close(self):
        self.s.close()


def newJob(type, data, hostname = 'localhost', port = 8787):
    qc = QueueClient(hostname, port)
    qc.enqueueJob(type,data)
    qc.close()
