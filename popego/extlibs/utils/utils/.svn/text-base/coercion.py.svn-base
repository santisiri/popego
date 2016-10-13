from inspect import getargspec
from itertools import izip

class CoercionError(Exception):
    """Raised when the coercion of any of the values given for coercion fails"""
    def __init__(self, *args, **kwargs):
        super(CoercionError, self).__init__(*args)
        self.kwargs = kwargs
    pass

def coerce_pairs(data, **kwtypes):
    """Enforces a type for each value in a list of (arg_name, value). Returns
    the new "coerced" list of (arg_name, coerced_value).

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    value in a dict whose key equals ``arg_name`` if its value is an instance of
    one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    d = []
    errs = {}
    for k,v in data:
        if not k in kwtypes:
            d.append((k, v))
            continue
        _types, _coercer = kwtypes[k]
        if any(isinstance(v, t) for t in _types):
            d.append((k, v))
            continue
        if k in kwtypes:
            try:
                coerced = _coercer(v)
            except Exception, e:
                errs[k] = e.message if hasattr(e, 'message') else repr(e)
                continue
            if not any(isinstance(coerced, t) for t in _types):
                raise ValueError('Bad Caster: %r should return an '
                        'instance of one of %r but returned %r' % (
                            _coercer, _types, coerced.__class__))
            d.append((k, coerced))
        else:
            d.append((k, v))
    if errs:
        raise CoercionError(**errs)
    return d

def coerce_dict(data, **kwtypes):
    """Enforces a type for each value in a dict. Returns the new "coerced" dict.

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    value in a dict whose key equals ``arg_name`` if its value is an instance of
    one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    return dict(coerce_pairs(dict(data).items(), **kwtypes))

def coerce_args(**kwtypes):
    """Destructive decorator that coerces a type for each arg given to a func.

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    argument passed to the function named ``arg_name`` if its value is an
    instance of one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    def check_accepts(f):
        def new_f(*args, **kwargs):
            def _get_xargs(f, a, d):
                d = d.copy()
                a = list(a)
                spec = getargspec(f)
                kwlen = len(spec[-1] or ())
                alen = len(spec[0]) - kwlen
                stack = list(spec[-1][::-1])
                out = []
                for i,x in enumerate(spec[0]):
                    if i < alen:
                        # dealing with a non-keyword arg
                        if len(a) >= alen:
                            # x is in a
                            out.append((x, a[i]))
                        else:
                            # x should be in d
                            out.append((x, d[x]))
                    else:
                        # dealing with a keyword arg
                        try:
                            out.append((x, d.get(x, stack.pop())))
                        except IndexError:
                            raise ValueError('Value missing for %s' % x)
                return out, alen
            xargs, alen = _get_xargs(f, args, kwargs)
            xargs = coerce_pairs(xargs, **kwtypes)
            _args = [x[1] for x in xargs[:alen]]
            _kwargs = dict(xargs[alen:])
            return f(*_args, **_kwargs)

        new_f.func_name = f.func_name
        return new_f
    return check_accepts
from inspect import getargspec
from itertools import izip

class CoercionError(Exception):
    """Raised when the coercion of any of the values given for coercion fails"""
    def __init__(self, *args, **kwargs):
        super(CoercionError, self).__init__(*args)
        self.kwargs = kwargs
    pass

def coerce_pairs(data, **kwtypes):
    """Enforces a type for each value in a list of (arg_name, value). Returns
    the new "coerced" list of (arg_name, coerced_value).

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    value in a dict whose key equals ``arg_name`` if its value is an instance of
    one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    d = []
    errs = {}
    for k,v in data:
        if not k in kwtypes:
            d.append((k, v))
            continue
        _types, _coercer = kwtypes[k]
        if any(isinstance(v, t) for t in _types):
            d.append((k, v))
            continue
        if k in kwtypes:
            try:
                coerced = _coercer(v)
            except Exception, e:
                errs[k] = e.message if hasattr(e, 'message') else repr(e)
                continue
            if not any(isinstance(coerced, t) for t in _types):
                raise ValueError('Bad Caster: %r should return an '
                        'instance of one of %r but returned %r' % (
                            _coercer, _types, coerced.__class__))
            d.append((k, coerced))
        else:
            d.append((k, v))
    if errs:
        raise CoercionError(**errs)
    return d

def coerce_dict(data, **kwtypes):
    """Enforces a type for each value in a dict. Returns the new "coerced" dict.

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    value in a dict whose key equals ``arg_name`` if its value is an instance of
    one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    return dict(coerce_pairs(dict(data).items(), **kwtypes))

def coerce_args(**kwtypes):
    """Destructive decorator that coerces a type for each arg given to a func.

    Given arguments as ``arg_name=(expected_types, coercer)`` verifies for each
    argument passed to the function named ``arg_name`` if its value is an
    instance of one of ``expected_types``. If not, coerce its value by calling
    ``coercer(value)`` which should return the value coerced to the
    ``expected_type``."""

    def check_accepts(f):
        def new_f(*args, **kwargs):
            def _get_xargs(f, a, d):
                d = d.copy()
                a = list(a)
                spec = getargspec(f)
                kwlen = len(spec[-1] or ())
                alen = len(spec[0]) - kwlen
                stack = list(spec[-1][::-1])
                out = []
                for i,x in enumerate(spec[0]):
                    if i < alen:
                        # dealing with a non-keyword arg
                        if len(a) >= alen:
                            # x is in a
                            out.append((x, a[i]))
                        else:
                            # x should be in d
                            out.append((x, d[x]))
                    else:
                        # dealing with a keyword arg
                        try:
                            out.append((x, d.get(x, stack.pop())))
                        except IndexError:
                            raise ValueError('Value missing for %s' % x)
                return out, alen
            xargs, alen = _get_xargs(f, args, kwargs)
            xargs = coerce_pairs(xargs, **kwtypes)
            _args = [x[1] for x in xargs[:alen]]
            _kwargs = dict(xargs[alen:])
            return f(*_args, **_kwargs)

        new_f.func_name = f.func_name
        return new_f
    return check_accepts
