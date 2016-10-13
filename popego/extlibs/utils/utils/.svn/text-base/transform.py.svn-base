# -*- coding: utf-8 -*-
"""
Modulo que permite construir diccionarios a través de un otro diccionario
y una definición de conversiones a realizar para cada clave requerida.

Un ejemplo sería:

>>> mapping = {'title': fromKey('mititulo'),
... 'siempreigual': constant(4)
... }

>>> transform(mapping, {'mititulo':'hola', 'siempreigual':'noimporta', 'nosirve':5})
{'siempreigual': 4, 'title': 'hola'}

También se puede definir transformers de la siguiente manera

>>> def sumar(k1,k2):
...     return lambda values: values[k1] + values[k2]
... 

>>> mapping = {'suma': sumar('a','b')}

>>> transform(mapping, {'a':40,'b':30})
{'suma': 70}

Otra opción es tener transformadores encadenados usando ``transformWith``

>>> submapping = {'title': fromKey('mititulo'),
'siempreigual': constant(4)
}

>>> mapping = {'suma': sumar('a','b'), 'otro': transformWith(submapping)}

>>> transform(mapping, {'a':40,'b':30, 'mititulo':'hola', 'siempreigual':'noimporta', 'nosirve':5})
{'otro': {'siempreigual': 4, 'title': 'hola'}, 'suma': 70}

"""
__docformat__='restructuredtext'


def transform(mapping, values):
    result = {}
    for k, transformer in mapping.items():
        result[k] = transformer(values)
    return result

# transformers
def constant(value):
    """ Transformer: Siempre retorna el mismo valor"""
    return lambda x: value

def ifKey(key, thencmd, elsecmd):
    """ Transformer: Si ``key`` existe llama a ``thencmd``, sino a ``elsecmd`` """
    return lambda vdict: thencmd(vdict) if key in vdict else elsecmd(vdict)

def constantCall(fn, args=[], kwargs={}):
    """ 
    Transformer: Llama al callable sin el diccionario.

    Opcionalmente, recibe argumentos posicionales y de clave para la
    llamada.
    """
    return lambda values: fn(*args, **kwargs)

def fromKey(key, *args):
    """ 
    Transformer: Retorna la clave ``key`` del diccionario.
    Recibe un segundo parametro opcional para indicar el default value en caso
    de no existir dicha clave.
    """
    if len(args) == 1:
        return lambda vdict: vdict.get(key, args[0])
    elif len(args) == 0:
        return lambda vdict: vdict[key]
    assert False, "1 or 2 arguments only"

def transformWith(mapping):
    """
    Transformer: Transforma el diccionario de entrada en uno de salida 
    utilizando el ``mapping``
    """
    return lambda values: transform(mapping, values)
