# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

def compose(*funcs, **kwargs):
    """ Returns a function which is the composition of the given functions.

        Usage: compose(f, g, h) returns a function equal to f(g(h))
    """   
    assert len(funcs) > 0
    def composed(*args,**kwargs):
        ret = funcs[-1](*args, **kwargs)
        for f in reversed(funcs[:-1]):
            ret = f(ret)
        return ret
    return composed
