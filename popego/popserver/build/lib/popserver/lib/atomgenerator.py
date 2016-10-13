# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elementtree import ElementTree as ET

def format_date(date):
    """ Recibe un datetime en UTC y lo formatea según RFC 3339 """
    return date.strftime("%Y-%m-%dT%H-%M-%SZ")

class AtomFeed(object):

    def __init__(self,id, title,updated):
        self.feed = ET.Element('feed',xmlns='http://www.w3.org/2005/Atom')
        ET.SubElement(self.feed,"id").text = str(id)
        ET.SubElement(self.feed,"title").text = title
        ET.SubElement(self.feed,"updated").text = format_date(updated)

    def addEntry(self, id, title, updated, summary):
        entry = ET.SubElement(self.feed,"entry")
        ET.SubElement(entry,"id").text = str(id)
        ET.SubElement(entry,"title").text = title
        ET.SubElement(entry,"updated").text = format_date(updated)
        ET.SubElement(entry,"summary").text = summary

    def toString(self):
        return ET.tostring(self.feed,'UTF-8')
