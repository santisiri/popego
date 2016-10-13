from pmock import *

class InvokedExactly(object):
    def __init__(self, expected):
        self.expected = expected
        self.count = 0
    def invoked(self, invocation):
        self.count +=1
    def matches(self, invocation):
        return True

    def verify(self):
        if self.expected != self.count:
            raise AssertionError("Expected %d invocation and got %d" 
                                 % (self.expected, self.count))

def exactly(n):
    return InvokedExactly(n)
