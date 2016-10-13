# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from elixir import session as dbsession, metadata
from popserver.lib.functional import memo
from popserver.model import TagCount, GlobalConfig
from sqlalchemy import text
from sqlalchemy.orm import eagerload
import logging

log = logging.getLogger(__name__)

@memo(1)
def getInterestAddFactor():
    return GlobalConfig.getAsInt('interest.tagInterestAddFactor')

@memo(1)
def getInterestThreshold():
    return GlobalConfig.getAsInt('interest.tagInterestThreshold')


def getUserTopInterests(user_id, qty):
    """ retorna una lista de Tag que representan los intereses de username """
    return TagCount.query.options(eagerload('tag')) \
        .filter(TagCount.user_id == user_id) \
        .filter(TagCount.interest_factor >= 0) \
        .order_by(TagCount.count.desc())[0:qty].all()
    
def isInterest(tag_name):
    """ ¿existe un ``Tag`` con nombre ``tag_name`` tal que sea un interés? """
    
    q = text(""" SELECT SUM(tagcounts.interest_factor)
                 FROM tagcounts, tags 
                 WHERE tags.id = tagcounts.tag_id AND tags.name = :tag
                 GROUP BY tagcounts.tag_id , tags.name 
                 HAVING SUM(tagcounts.interest_factor) >= :threshold """)

    return metadata.bind.execute(q, tag=tag_name, threshold=getInterestThreshold()).rowcount > 0

def setInterestDown(tag_count):
    _setInterest(tag_count, getInterestAddFactor() * -1)

def setInterestUp(tag_count):
    _setInterest(tag_count, getInterestAddFactor())
    
def _setInterest(tag_count, interest_value):
    tag_count.interest_factor = interest_value
    dbsession.flush()

