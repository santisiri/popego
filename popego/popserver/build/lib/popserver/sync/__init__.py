# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import datetime
from popserver.model import Tag, UserItem
from sqlalchemy.orm import object_session

def mergeItem(item, service):
    """
    Dado un ``item`` se fija si ya existe en la base.
    Si existe saca de la session a ``item`` y usa el de la base.
    De no existir le anexa el servicio
    """
    dbItem = item.__class__.query.filter_by(external_id=item.external_id, service=service).first()
    if dbItem is None:
        dbItem = item
        dbItem.service = service
        for i in range(0, len(dbItem.tags)):
            dbItem.tags[i] = mergeTag(dbItem.tags[i])
    else:
        item.expunge()
        
    return dbItem


def mergeTag(tag):
    dbTag = Tag.get_by(name=tag.name)
    if dbTag is not None:
        if object_session(tag) is not None: tag.expunge()
        tag = dbTag
        
    return tag


def mergeUserItem(userItem, account):
    """ Mergea el UserItem y el Item asociado """
            
    userItem.item = mergeItem(userItem.item, account.service)
    if userItem.item.id is not None:
        userItem = _mergeUserItemInstance(userItem, account.user)
        
    # En UserItem se mergean los tags propios del UserItem (UserItem._tags).
    # No se usa UserItem.tags porque sino se estarían copiando tags del Item
    # al UserItem 
    for i in range(0, len(userItem._tags)):
        userItem._tags[i] = mergeTag(userItem._tags[i])
                
    userItem.user = account.user
            
    return userItem


def _mergeUserItemInstance(userItem, user):
    """ Mergea solo la instancia de UserItem """
            
    dbUserItem = UserItem.query.filter_by(user=user, item=userItem.item).first()
    if dbUserItem is None:
        dbUserItem = userItem
    else:
        userItem.expunge()
                
    return dbUserItem
