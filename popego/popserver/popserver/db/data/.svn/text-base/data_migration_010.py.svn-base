# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# cambio de nombre de service type

migration = [
    ("""
         UPDATE service_types 
           SET type = 'pictures'
           WHERE type = 'photos';
     """, 
     """
        SELECT 1;
     """),
]