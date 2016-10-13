# -*- coding: utf-8 -*-
"""
Modulo responsable de syncronizar los ``Account``s de cada ``User`` con la 
información disponible en cada ``Service``.

Su API pública consiste en:
 * updateAccount(account)

Se asume un API para el agente:
 * agent.updateAccount(account, cacheapi)

"""

__docformat__='restructuredtext'

from datetime import datetime
from popserver.model import dbsession, UserItem, ItemGroup
from sqlalchemy import text
from popserver.sync import mergeItem, mergeUserItem
import logging

NULL_GROUP_ID = '__ferEstoEsParaVos__'
FLUSH_COUNT = 30


def updateAccount(account):
    """ 
    Sincroniza la información ya existente en la BD con la información
    disponible en el Servicio.

    Utiliza el ``Agent`` y el ``UserItemFactory`` del Servicio
    """
    agent = account.service.getAgent()
    cacheApi = CacheAPI(account)
    cacheApi.start()
    agent.updateAccount(account,cacheApi)
    cacheApi.end()


class CacheAPI(object):
    """
    API para ser usada por los agentes.
    Representa la forma de los agentes de indicar al Cache el resultado
    de parsear el contenido del servicio
    """
    def __init__(self, account):
        self.account = account
        self.userItemFactory = account.service.getUserItemFactory(account.user)
        self.flushCount = 0

    def start(self):
        self.groups  = dict()
        self.userItems = dict()

        for g in self.account.item_groups:
            self.groups[g.external_id] = g
            for ui in g.items:
                self.userItems[ui.item.external_id] = ui
        

    def groupExists(self, extId):
        """ Indica si existe un grupo identificado por ``extId``(externalId) """
        if extId is None: extId = NULL_GROUP_ID
        return extId in self.groups

    def itemExists(self, extId):
        """ 
        Indica si existe un userItem cuyo Item este identificado
        por ``extId`` (externalId)
        """
        return extId in self.userItems

        
    def addGroup(self, extId, **attrs):
        """
        Agrega un grupo al cache, identificado por ``extId``, donde
        ``attrs`` es un mapa de sus atributos.

        Usar ``None`` para el grupo Nulo
        """
        if not self.groupExists(extId):
            logging.info("Adding Group %s, %s" % (attrs['name'],extId))

            if extId is None: extId = NULL_GROUP_ID
            g = ItemGroup(external_id=extId,**attrs)
            self.account.item_groups.append(g)
            self.groups[extId] = g

    def addItem(self, extId, attrs):
        """
        Agrega un userItem y un item al cache, identificado por ``extId``, 
        donde ``attrs`` es un mapa de sus atributos (del userItem y del item)
        """
        userItem = self.userItemFactory.create(extId, attrs)
        self.userItems[extId] = userItem

    def removeItemFromGroup(self, gExtId, iExtId):
        """
        Remueve la asociación de un UserItem con un Group
        """
        if gExtId is None: gExtId = NULL_GROUP_ID
        g = self.groups[gExtId]
        ui = self.userItems[iExtId]

        # del self.userItems[iExtId]
        g.items.remove(ui)
        
    def clearItemsFromGroup(self, gExtId):
        """
        Remueve todos los UserItems de un Group
        """
        if gExtId is None: gExtId = NULL_GROUP_ID
        g = self.groups[gExtId]
        g.items = []

    def bindItem2Group(self, gExtId, iExtId):
        """
        Realiza el Binding entre un UserItem y un Grupo, identificados
        por sus respectivos external ids

        """
        if gExtId is None: gExtId = NULL_GROUP_ID
        g = self.groups[gExtId]
        ui = self.userItems[iExtId]

        if ui not in g.items:
            g.items.append(ui)

            self.flushCount +=1
            if self.flushCount % FLUSH_COUNT == 0:
                dbsession.flush()
                logging.info("Flushed %d Items" % FLUSH_COUNT)


    def groupItems(self, extId):
        if extId is None: extId = NULL_GROUP_ID
        return [ui.item.external_id for ui in self.groups[extId].items]

    def end(self):
        """ Evento para señalar el fin de la sincronización"""
        self.account.last_updated = datetime.utcnow()
        dbsession.flush()

        del self.groups
        del self.userItems
        del self.account
        logging.info("Update Finished")
