# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
""" Tests para utility functions y helpers. No requiren fixtures ni inicializar nada """

import unittest
from datetime import datetime
from datetime import timedelta
from popserver.lib.util import interval_of_time_in_words

class TestIntervalOfTimeInWords(unittest.TestCase):

    def test_intervalOfTimeInWords(self):
        from_time = datetime.utcnow()
        assert interval_of_time_in_words(from_time, from_time + timedelta(minutes=50)) == 'about an hour'
        assert interval_of_time_in_words(from_time, from_time + timedelta(seconds=15)) == 'less than a minute'
        assert interval_of_time_in_words(from_time, from_time + timedelta(days=1095.75)) == 'over 3 years'
        assert interval_of_time_in_words(from_time, from_time + timedelta(hours=60)) == '2 days'
        assert interval_of_time_in_words(from_time, from_time + timedelta(seconds=76)) == '1 minute'
        assert interval_of_time_in_words(from_time, from_time + timedelta(days=368)) == 'about 1 year'
        assert interval_of_time_in_words(from_time, from_time + timedelta(days=1500)) == 'over 4 years'
