# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.model import GlobalConfig
import pickle, elixir
from sqlalchemy import text

query = text("""
select sum(diff) as dist from (
  select max((coalesce(tc."weightedCount", 0) + 5) / (10 + ut.woc)) 
         - min((coalesce(tc."weightedCount", 0) + 5) / (10 + ut.woc)) as diff 
    from tagcounts tc right outer join (
        select u.id as uid, t.id as tid, u."weightedObjCount" as woc 
        from tags t,users u
      ) ut on tc.tag_id = ut.tid and tc.user_id = ut.uid
    group by ut.tid
  ) as a
""")


class UpdateCompatibilityRanges(object):

    def start(self):
        distance  = self.computeMaxDistance()
        qty = int(GlobalConfig.get('interest.nroOfCompatibilityRanges').value)
        step = distance / qty
        ranges = range(0,distance+1, step)
        
        gc = GlobalConfig.get('interest.compatibilityRanges')
        if gc is None:
            gc = GlobalConfig(property='interest.compatibilityRanges')
        gc.value = pickle.dumps(ranges)

        gc.flush()
        
    def createRanges(self, distance, qty):
        ranges = []
        step = distance / qty
        curr = 0
        for i in xrange(0,qty):
            curr += step
            ranges.append(curr)
        return ranges

    def computeMaxDistance(self):
        # Se obtiene una conexión
        conn = elixir.metadata.bind.connect()
        
        # Se ejecuta pasandole los parámetros y devuelve una lista de tuplas
        distance = conn.execute(query).fetchone()[0]
        return distance
