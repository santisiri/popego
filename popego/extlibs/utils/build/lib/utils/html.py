# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import HTMLParser

__all__=['stripHTMLTags']

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
