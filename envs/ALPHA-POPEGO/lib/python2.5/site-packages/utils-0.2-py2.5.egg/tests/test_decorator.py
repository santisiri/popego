from unittest import TestCase
from utils.decorator import *

class FailUntil(object):
    def __init__(self, fails, exception=Exception):
        self.fails = fails
        self.calls = 0
        self.exception = exception

    def __call__(self, retValue):
        self.calls +=1
        if self.calls <= self.fails:
            raise self.exception
        else:
            return retValue



class TestRetryDecoraton(TestCase):

    def test_noRetry(self):
        fn = retry(0,Exception)(FailUntil(0))
        self.assertEqual(10, fn(10))

        fn = retry(0,Exception)(FailUntil(1))
        self.assertRaises(Exception, fn, 10)

    def test_oneRetry_success(self):
        fn = retry(1,Exception)(FailUntil(1))
        self.assertEqual(10, fn(10))

    def test_oneRetry_failure(self):
        fn = retry(1,Exception)(FailUntil(2))
        self.assertRaises(Exception, fn, 10)

    def test_severalRetries_success(self):
        fn = retry(10,Exception)(FailUntil(10))
        self.assertEqual(10, fn(10))

    def test_severalRetries_failure(self):
        fn = retry(10,Exception)(FailUntil(11))
        self.assertRaises(Exception, fn, 10)

    def test_severalException_success(self):
        fn = retry(10,ZeroDivisionError, AttributeError) \
            (FailUntil(10,ZeroDivisionError))
        self.assertEqual(10, fn(10))

    def test_severalException_failure(self):
        fn = retry(10,ZeroDivisionError, AttributeError) \
            (FailUntil(11,ZeroDivisionError))
        self.assertRaises(ZeroDivisionError, fn, 10)

        fn = retry(10,ZeroDivisionError, AttributeError) \
            (FailUntil(11, AttributeError))
        self.assertRaises(AttributeError, fn, 10)
