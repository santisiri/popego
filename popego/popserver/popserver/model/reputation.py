# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import functools
import operator
from popserver.model import GlobalConfig
import pickle

class PopegoIntelligence(object):
    def __init__(self):
        self.tagCount = Tag.query.count()
        self.baseProb = 0.5
        self.baseProbWeight = 10
        self.compatibilityIntervals = pickle.loads(
            GlobalConfig.get('interest.compatibilityRanges').value)

    def distance(self, u1, u2):
        """ Calcula la distancia manhattan entre dos usuarios """
        ip1 = InterestProfile(self, u1)
        ip2 = InterestProfile(self, u2)
        
        nonZeroTags = set(ip1.nonZeroTags() + ip2.nonZeroTags())
        zeroTagsCount = self.tagCount - len(nonZeroTags)

        # calculates manhatan distance
        distance = zeroTagsCount * abs(ip1.baseProb() - ip2.baseProb())
        for t in nonZeroTags:
            distance += abs(ip1.prob(t) - ip2.prob(t))
        return distance
        
    def compatibilityRank(self, u1, u2):
        distance = self.distance(u1, u2)
        for i,v in enumerate(self.compatibilityIntervals):
            if v > distance:
                return i
        raise Exception("distance out of range")

    def interestForUser(self, u1, u2):
        ip1 = InterestProfile(self, u1)
        ip2 = InterestProfile(self, u2)
        
        nonZeroTags = set(ip1.nonZeroTags() + ip2.nonZeroTags())
        zeroTagsCount = self.tagCount - len(nonZeroTags)

        baseRelevance, relDict = ip1.relevance(self.tagCount)
        
        accum =  abs(zeroTagsCount * baseRelevance * 
                     (ip1.baseProb() - ip2.baseProb()))

        for t in nonZeroTags:
            relevance = relDict.get(t, baseRelevance)
            accum += abs(relevance * (ip1.prob(t) - ip1.prob(t)))

        return accum

class InterestProfile(object):
    def __init__(self, pi, u):
        self.pi = pi
        self.objCount = u.weightedObjCount
        self.tags = dict((tc.tag,tc.weightedCount) for tc in u.tagCounts)

    def nonZeroTags(self):
        """ Tags que esten al menos en un item """
        return self.tags.keys()

    def baseProb(self):
        """ Probabilidad base. Es la probabilidad para tags q no tiene el usr"""
        return self._probForCount(0)

    def prob(self, tag):
        """ Probabilidad de un tag """
        return self._probForCount(self.tags.get(tag,0))

    def _probForCount(self, count):
        return self.pi.baseProb * self.pi.baseProbWeight + count \
            / (self.pi.baseProbWeight + self.objCount)

    def relevance(self, totalTags):
        zeroTags = totalTags - len(self.tags)
        baseProb = self.baseProb()
        totalSum = float(zeroTags * baseProb)
        for t in self.tags:
            totalSum += self.prob(t)
        
        rel = {}
        for t in self.tags:
            rel[t] = self.tags[t] / totalSum
        
        baseRelevance = baseProb / totalSum

        return baseRelevance, rel
