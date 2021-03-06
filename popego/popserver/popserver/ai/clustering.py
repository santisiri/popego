# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from numpy import linalg, zeros, diag
from popserver.model import GlobalConfig
from popserver.ai.base import kMeans, randomCentroids
from math import sqrt
import elixir
from sqlalchemy import text


EPSILON = 1e-5


def toTransitionMatrix(W):
    """ W: numpy.array instance """
    transitionMatrix = W.copy()
    rowSum = transitionMatrix.sum(axis=1)
    n, m = transitionMatrix.shape
    for i in range(n):
        For j in range(m):
            transitionMatrix[i,j] = W[i,j] / rowSum[i]

    return transitionMatrix


def isAllOneEigenvector(v):
    """ Checks if `v` is the all-ones eigenvector or is lialmost dependent"""
    if len(v) > 1:
        for i in range(len(v)-1):
           if abs(v[i] - v[i+1]) > EPSILON:
              return False

    return True


def computeEigenvectorMatrix(W, K):
    """ Computes the top K - 1 eigenvectors (ignoring the trivial all-ones
        eigenvector) from matrix W"""
    if W.shape[0] != W.shape[1] or K <= 1  or  K > W.shape[0]:
        raise Exception("Invalid Input")

    evals, evects = linalg.eig(W) 
    print (evals, evects)
    
    evalsIndexes = [(i, abs(evals[i])) for i in range(len(evals))]
    sortedEvals = sorted(evalsIndexes, lambda a, b: cmp(a[1], b[1]), 
                            reverse=True)

    print sortedEvals
    topEvalsIndexes = []
    k = 0
    for i in range(evects.shape[1]):
        if not isAllOneEigenvector(evects[:,sortedEvals[i][0]]):
            topEvalsIndexes.append(sortedEvals[i][0])
            k += 1
            if k == K - 1:
                break
    return evects[:,topEvalsIndexes]


def normalizeRows(M):
    """ Normalizes the rows of M using the l2-norm"""
    for i in range(len(M)):
        vNorm = linalg.norm(M[i])
        if vNorm != 0:
            M[i] =  M[i] / vNorm


def almostOrthogonalCentroids(rows, k):
    assert k > 1
    assert k - 1 == len(rows[0])
    
    centroids = [[1.0 if i==j else 0.0 for i in range(k-1)] for j in range(k-1)]
    centroids.append([-1.0 / sqrt(k-1) for i in range(k-1)])

    return centroids    


def clusterModularity(W, partition):
    """ Computes the modularity of a given ``partition`` """    
    weightSum = W.sum()
    modularity = 0.0

    for i, cluster in enumerate(partition):
        # TODO Hacer todo en una unica barrida de la matrix
        intraClusterSum = sum([ W[i][j] for i in cluster for j in cluster ])

        # TODO cual de las dos cuentas es?
        #clusterAttachedSum = sum([ W[i][j] for i in cluster 
        #                                    for j in range(W.shape[1]) if j not in cluster ])
        clusterAttachedSum = sum([ W[i][j] for i in cluster 
                                            for j in range(W.shape[1]) ])
        modularity += intraClusterSum / weightSum - (clusterAttachedSum / weightSum) ** 2

    return modularity


def spectral1Cluster(W, k1, k2):
    if k1 < 1 or k2 < k1:
        raise Exception('Invalid k-range')

    transitionMatrix = toTransitionMatrix(W)
    U_K = computeEigenvectorMatrix(transitionMatrix, k2)   
    assert U_K.shape == (W.shape[0], k2-1)
    del transitionMatrix
    print U_K

    maxModularity = -1.0
    bestCluster = None
    for k in range(k1, k2 + 1):
       U_k = U_K[:,:k-1].copy()
       normalizeRows(U_k) 
       clusters = kMeans(U_k, k, initCentroids=almostOrthogonalCentroids)
       currModularity = clusterModularity(W, map(lambda t: t[1], clusters))
       print "k: %d - modularity: %f" % (k, currModularity)
       print clusters
       if currModularity > maxModularity:
            maxModularity = currModularity
            bestCluster = clusters
       
    return bestCluster







def getAllInterests():
    # TODO Cambiar para que tome los intereses
    conn = elixir.metadata.bind.connect()
    s = text("""select id from tags order by id""")
    return map(lambda t: t[0], conn.execute(s).fetchall())
    

def iterInterestsByItem(iteminterests):
    if len(iteminterests) > 0:
        currentItem = iteminterests[0][0]
        interests = [iteminterests[0][1]]
        for item, interest in iteminterests[1:]:
            if item is currentItem:
                interests.append(interest)
            else:
                currentItem = item
                if len(interests) > 1:
                    yield interests
                interests = [interest]
        if len(interests) > 1:
            yield interests

     

def getItemInterestsLists():
    # TODO Cambiar para que tome los intereses
    iteminterestsQueries = [text("""select user_items_id, tags_id
                from tags_useritems
                order by user_items_id"""),
               text("""select items_id, tags_id
                from tags_items
                order by items_id""")]

    conn = elixir.metadata.bind.connect()
    for query in iteminterestsQueries:
        yield conn.execute(query).fetchall()
   

def reverseIndex(t):
    return t[1], t[0]


def computeSimilarity(simMatrix, interests, interestsDict):
    for i in range(len(interests)-1):
        for j in range(i+1, len(interests)):
            index = (interestsDict[interests[i]], interestsDict[interests[j]])
            #simMatrix[index] += 1.0
            #simMatrix[reverseIndex(index)] += 1.0
            if simMatrix[index[0]][index[1]] == 0:
                simMatrix[index[0]][index[1]] = 1
                simMatrix[index[1]][index[0]] = 1


def createInterestsSimilarityMatrix():
    allInterests = getAllInterests()
    interestsDict = dict(map(lambda t: (t[1], t[0]), enumerate(allInterests)))
    # TODO Optimize for sparse and symmetric matrices
    #simMatrix = zeros( (len(allInterests), len(allInterests)) )
    #simMatrix = diag( [1.0 for i in range(len(allInterests))] )
    simMatrix = [ [0 for i in range(len(allInterests))] for j in range(len(allInterests)) ]
    
    for iteminterests in getItemInterestsLists():
        for interests in iterInterestsByItem(iteminterests):
            computeSimilarity(simMatrix, interests, interestsDict)
                
    return (allInterests, simMatrix)
        


from igraph import Graph, ADJ_LOWER

def igraphCluster(allInterests, simMatrix):
    g = Graph()
    g = g.Adjacency(simMatrix, ADJ_LOWER)
    for i, v in enumerate(g.vs):
       v['interest_id'] = allInterests[i]
    
    cl = g.community_fastgreedy()
    
    return [ extractVertexIds(cl.subgraph(i))  for i in range(len(cl.sizes())) ]


def extractVertexIds(g):
    return [ v['interest_id'] for v in g.vs ]
    

        
    
