# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.model import GlobalConfig, Compatibility

import pickle, elixir
from sqlalchemy import text, types, UniqueConstraint
from popserver.ai.base import kMeans

__all__ = ['updateDb', 'compatibilityFor']

DISTANCE_QUERY = text("""
select sum(@(p1.prob - p2.prob)) as dist, p1.uid, p2.uid 
  from
    (select coalesce(tc."weightedCount", 0) / ut.woc as prob,
            ut.uid as uid, ut.tid as tid
       from tagcounts tc right outer join 
            (select u.id as uid, t.id as tid, u."weightedObjCount" as woc
               from tags t,users u
	       where u."weightedObjCount" >= :objThreshold) 
            ut on tc.tag_id = ut.tid and tc.user_id = ut.uid
    ) as p1,
    (select coalesce(tc."weightedCount", 0) / ut.woc as prob,
            ut.uid as uid, ut.tid as tid
       from tagcounts tc right outer join 
            (select u.id as uid, t.id as tid, u."weightedObjCount" as woc 
               from tags t,users u
	       where u."weightedObjCount" >= :objThreshold)
            ut on tc.tag_id = ut.tid and tc.user_id = ut.uid
    ) as p2
  where p1.uid > p2.uid and p1.tid = p2.tid
  group by p1.uid, p2.uid
  order by dist
""")

def compatibilityFor(user1, user2):
    """ Retorna el porcentaje de compatibilidad entre dos usuarios """
    id1, id2 = (user1.id, user2.id) if user1.id > user2.id  \
        else (user2.id, user1.id)
    if id1 == id2: return 100

    comp = Compatibility.get_by(user1_id=id1,user2_id=id2)

    if comp is None:
        return None
    else:
        return comp.compatibility

def updateDb():
    """ Realiza la actualización de todas las compatibilidades """
    threshold = GlobalConfig.getAsInt('compatibility.objCountThreshold')
    distances = computeDistances(threshold)

    if len(distances) > 0:
        normDistances = normalizeDistances(distances)
    
        for c in Compatibility.query.all():
            c.delete()

        for comp, user1, user2 in normDistances:
            Compatibility(compatibility=comp,user1_id=user1,user2_id=user2)
        elixir.session.flush()


def computeDistances(objCountThreshold):
    """ 
    Calcula las distancias de todos los usuarios con todos los usuarios.
    Retorna una lista de tuplas con la forma (dist, userId1, userId2)
    """

    # Se obtiene una conexión
    conn = elixir.metadata.bind.connect()
        
    # Se ejecuta pasandole los parámetros y devuelve una lista de tuplas
    distances = conn.execute(DISTANCE_QUERY,objThreshold=objCountThreshold) \
        .fetchall()
    return distances


def normalizeDistances(distances):
    maxValue = max(map(node2Value, distances))
    
    return [(int((1 - (dist / maxValue)) * 100), u1, u2) for dist, u1, u2 
            in distances]
        

def clusterizeDistances(initCentroids, distances, clustersNro):
    """ 
    Crea ``clustersNro`` clusters sobre la lista de distancias
    de usuarios. De esta forma, las distancias entre usuarios
    caen en ``clustersNro`` categorías.
    
    Para clusterizar, utiliza KMeans. ``initCentroids`` es 
    una funcion que indica las centroides iniciales a utilizar.
    """
    
    def distance(t1,t2):
        """ Distance function """
        return abs(t1 - t2)

    return kMeans(distances, clustersNro, distance, initCentroids)
        


def node2Value(node): 
    return node[0]



# Centroid initialization Functions
def uniformCentroids(nodes, clustersNro):
    """ Lo divide en n intervalos equidistantes"""
    interval = (node2Value(nodes[0]), node2Value(nodes[-1]))
    step = (interval[1] - interval[0]) / clustersNro
    centroids = range(interval[0],interval[1]+1, step)[:clustersNro]
    assert len(centroids) == clustersNro
    return centroids

def statisticalCentroids(nodes, clustersNro):
    """ Lo divide en mediana/cuartil/decil/N_il """
    step = len(nodes) / clustersNro
    return [node2Value(nodes[i*step]) for i in range(0,clustersNro)]

##


def displayDistances(distances):
    """ Helper function to print computed Distances """
    print "Distances:"
    print "User1\tUser2\tDistance"
    for dist, u1, u2 in distances:
        print "%s\t%s\t%s" % (User.get(u1), User.get(u2), dist)

