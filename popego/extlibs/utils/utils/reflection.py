# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import types, os

def pathToObject(path):
    if ':' in path:
        modulePath,attrs = path.split(':',1)

        needsCall = False
        if attrs.endswith('()'):
            attrs = attrs[:-2]
            needsCall = True
        attrs = attrs.split(".")
        obj = __import__(modulePath, fromlist=['__name__'])

        for attr in attrs:
            obj = getattr(obj, attr)
        if needsCall:
            obj = obj()
    else:
        obj = __import__(path, fromlist=['__name__'])

    return obj

def importModule(modulepath):
    """ Imports a module given a modulepath """
    return __import__(modulepath, fromlist=['__name__'])


def findClasses(module, predicate=lambda name, klass: True):
    """ 
    Finds classes in a module. Returns [(ClassName, Class)]
    
    If ``predicate`` is given, returns classes matching
    that predicate. A predicate recieves an module attr name and a class

    The ``module`` parameter can be a module or a modulepath
    """

    if isinstance(module, str):
        module = importModule(module)

    return [(name, obj) for name, obj in vars(module).items()
            if isClass(obj) and predicate(name, obj)]

def isValidClass(classpath):
    """ 
    Given a ``classpath`` (format: my.module.path:MyClassName), it indicates
    if the class exists (and it's a class)
    """
    modulepath, classname = classpath.split(':',1)
    try:
        m = importModule(modulepath)
        print "this is %s" % getattr(m, classname)
        return isClass(getattr(m, classname))
    except ImportError:
        return False

def getObject(objpath):
    """
    Given an ``objpath`` (format: my.module.path:moduleattr), it returns
    the obj corresponding to that path
    """
    modulepath, attrname = objpath.split(':',1)
    m = importModule(modulepath)
    return getattr(m, attrname)

def isClass(obj):
    """ Indicates if ``obj`` is a class """
    objtype = type(obj)
    return objtype is types.ClassType or issubclass(objtype, type)

def findSubModules(module):
    """
    Recieves a ``module``, and return any direct submodules relative names if they exists.
    
    ``module`` can be a module path
    """
    if isinstance(module, str):
        module = importModule(module)
    if not module.__file__.endswith('__init__.pyc'):
        return []
    
    basepath = os.path.abspath(os.path.dirname(module.__file__))

    modules = []
    for filename in os.listdir(basepath):
        if filename != "__init__.py" and filename.endswith('.py'):
            modules.append(filename[:-3])
        elif os.path.isfile(os.path.join(basepath, filename, '__init__.py')):
            modules.append(filename)

    return modules



