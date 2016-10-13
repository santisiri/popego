import re
import time
import datetime
import HTMLParser

def strToDatetime(str):
    return datetime.datetime(*_parse_date_w3dtf(str)[0:6])

# Taken from the universal feed parser http://feedparser.org
# modified to support .000 after the seconds

# W3DTF-style date parsing adapted from PyXML xml.utils.iso8601, written by
# Drake and licensed under the Python license.  Removed all range checking
# for month, day, hour, minute, and second, since mktime will normalize
# these later
def _parse_date_w3dtf(dateString):
    def __extract_date(m):
        year = int(m.group('year'))
        if year < 100:
            year = 100 * int(time.gmtime()[0] / 100) + int(year)
        if year < 1000:
            return 0, 0, 0
        julian = m.group('julian')
        if julian:
            julian = int(julian)
            month = julian / 30 + 1
            day = julian % 30 + 1
            jday = None
            while jday != julian:
                t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
                jday = time.gmtime(t)[-2]
                diff = abs(jday - julian)
                if jday > julian:
                    if diff < day:
                        day = day - diff
                    else:
                        month = month - 1
                        day = 31
                elif jday < julian:
                    if day + diff < 28:
                       day = day + diff
                    else:
                        month = month + 1
            return year, month, day
        month = m.group('month')
        day = 1
        if month is None:
            month = 1
        else:
            month = int(month)
            day = m.group('day')
            if day:
                day = int(day)
            else:
                day = 1
        return year, month, day

    def __extract_time(m):
        if not m:
            return 0, 0, 0
        hours = m.group('hours')
        if not hours:
            return 0, 0, 0
        hours = int(hours)
        minutes = int(m.group('minutes'))
        seconds = m.group('seconds')
        if seconds:
            import math
            seconds = int(math.floor(float(seconds)))
        else:
            seconds = 0
        return hours, minutes, seconds

    def __extract_tzd(m):
        '''Return the Time Zone Designator as an offset in seconds from UTC.'''
        if not m:
            return 0
        tzd = m.group('tzd')
        if not tzd:
            return 0
        if tzd == 'Z':
            return 0
        hours = int(m.group('tzdhours'))
        minutes = m.group('tzdminutes')
        if minutes:
            minutes = int(minutes)
        else:
            minutes = 0
        offset = (hours*60 + minutes) * 60
        if tzd[0] == '+':
            return -offset
        return offset

    __date_re = ('(?P<year>\d\d\d\d)'
                 '(?:(?P<dsep>-|)'
                 '(?:(?P<julian>\d\d\d)'
                 '|(?P<month>\d\d)(?:(?P=dsep)(?P<day>\d\d))?))?')
    __tzd_re = '(?P<tzd>[-+](?P<tzdhours>\d\d)(?::?(?P<tzdminutes>\d\d))|Z)'
    __tzd_rx = re.compile(__tzd_re)
    __time_re = ('(?P<hours>\d\d)(?P<tsep>:|)(?P<minutes>\d\d)'
                 '(?:(?P=tsep)(?P<seconds>\d\d(?:[.,]\d+)?))?'
                 + __tzd_re)
    __datetime_re = '%s(?:T%s)?' % (__date_re, __time_re)
    __datetime_rx = re.compile(__datetime_re)
    m = __datetime_rx.match(dateString)
    if (m is None) or (m.group() != dateString): return
    gmt = __extract_date(m) + __extract_time(m) + (0, 0, 0)
    if gmt[0] == 0: return
    return time.gmtime(time.mktime(gmt) + __extract_tzd(m) - time.timezone)

def interval_of_time_in_words(from_time, to_time):
    """ port of Rails' ActionView::Helpers::DateHelper.distance_of_time_in_words """
    delta = abs(to_time - from_time)
    distance_in_seconds = (delta.days * 86400) + (delta.seconds)
    distance_in_minutes = distance_in_seconds / 60

    interval = ''

    if distance_in_minutes in range(0,2):
        return 'less than a minute' if distance_in_minutes == 0 else '1 minute'
    if distance_in_seconds in range(0, 5):
        interval = 'less than 5 seconds'
    elif distance_in_seconds in range(5, 10):
        interval = 'less than 10 seconds'
    elif distance_in_seconds in range(10, 20):
        interval = 'less than 20 seconds'
    elif distance_in_seconds in range(20, 40):
        interval = 'half a minute'
    elif distance_in_seconds in range(40, 60):
        interval = 'minute'
    elif distance_in_minutes in range(2, 45):
        interval = '%s minutes' % distance_in_minutes
    elif distance_in_minutes in range(45, 90):
        interval = 'about an hour'
    elif distance_in_minutes in range(90, 1440):
        interval = 'about %s hours' % (distance_in_minutes / 60)
    elif distance_in_minutes in range(1440, 2880):
        interval = '1 day'
    elif distance_in_minutes in range(2880, 43200):
        interval = '%s days' % (distance_in_minutes / 1440)
    elif distance_in_minutes in range(43200, 86400):
        interval = 'about 1 month'
    elif distance_in_minutes in range(86400, 525600):
        interval = '%s months' % (distance_in_minutes / 43200)
    elif distance_in_minutes in range(525600, 1051199):
        interval = 'about 1 year'
    else:
        interval = 'over %s years' % (distance_in_minutes / 525600)

    return interval


class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)

def stripHTMLTags(text):
    stripper = MLStripper()
    stripper.feed(text)
    return stripper.get_fed_data()
