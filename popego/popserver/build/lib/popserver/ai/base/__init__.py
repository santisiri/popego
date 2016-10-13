# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from math import sqrt
import random


def euclidean(v1, v2):
    """ Returns the euclidean distance of ``v1`` and ``v2`` """
    assert len(v1) == len(v2)
    
    return sqrt(sum([pow(v1[i]-v2[i], 2) for i in range(len(v1))]))



def randomCentroids(rows, k):
    """ Computes ``k`` random centroids contained on the given ``rows``"""

    # Determine the minimum and maximum values for each point
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
    for i in range(len(rows[0]))]
    
    # Create k randomly placed centroids
    centroids=[[random.random( )*(ranges[i][1]-ranges[i][0])+ranges[i][0]
    for i in range(len(rows[0]))] for j in range(k)]

    assert len(centroids) == k 
    
    return centroids



def kMeans(rows, k=4, distance=euclidean, initCentroids=randomCentroids):
    """ 
    Creates ``k`` clusters from ``rows`` using the k-means algorithm. 
    
    Arguments:
      * ``rows``: Data to cluster. Must be enumerable. 
            All the rows must have the same lenght.
      * ``k``: Number of clusters to create
      * ``distance``: Function that measures the distance between two ``rows``
      * ``initCentroids``: Function that returns the initial set of centroids
        used by the k-means algoritm 
    """
    dim = len(rows[0])
    # initial centroids position 
    centroids = initCentroids(rows, k)
    # iterate until no centroid change or 100 loops passed
    lastmatches = None
    for t in range(100):
        bestmatches = [[] for i in range(k)]
        
        # Find wich centroid is the closest for each row
        for j, row in enumerate(rows):
            bestmatch = 0
            for i, centroid in enumerate(centroids):
                d = distance(row, centroid)
                if d < distance(row, centroids[bestmatch]):
                    bestmatch = i
            bestmatches[bestmatch].append(j)
            
        if bestmatches == lastmatches: break
        lastmatches = bestmatches

        # Move the centroids to the average of their members
        for i, matchs in enumerate(bestmatches):
            nMatchs = len(matchs)
            if nMatchs > 0:
                centroids[i] = [sum(map(lambda t:rows[t][j], matchs)) / nMatchs for j in range(dim)]
        
    return zip(centroids, bestmatches)


