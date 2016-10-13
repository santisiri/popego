# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

from popserver.ai import compatibility

__jobDescription__ = """
Actualiza los calculos de compatibilidad de todos los usuarios
"""

def start(*args):
    compatibility.updateDb()
