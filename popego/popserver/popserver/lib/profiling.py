import gc

def isInModules(*names):
    def _isModule(obj):
        return getModule(obj) in names
    return _isModule

def getModule(obj):
    if getattr(obj, '__module__', None) is not None:
        module_parts = obj.__module__.split('.')
        module = '.'.join(module_parts[:3])
        return module
    return None
    

def isInstance(obj):
    if hasattr(obj, '__class__'):
        # new style classes
        _isInstance = not issubclass(obj.__class__, type)
    else:
        import types
        _isInstance = type(obj) == types.InstanceType
    return _isInstance

plus = lambda x,y: x+y

def groupBy(hash, objs, agregator=None):
    def defaultAgregator(aList, x):
        aList.append(x)
        return aList
    if agregator is None:
        agregator = defaultAgregator

    groups = {}
    for o in objs:
        h = hash(o)
        groups.setdefault(h, [])
        groups[h] = agregator(groups[h], o)
    return groups


class GCReport(object):
    def __init__(self):
        self._previous = {}

    def objectsInModules(self, *moduleNames):
        return filter(isInModules(*moduleNames), gc.get_objects())

    def report_objects(self, threshold=500):
        objects = gc.get_objects()
        print "Number of objects in memory: %d" % len(objects)
        modules = {}
        for obj in gc.get_objects():
            if getattr(obj, '__module__', None) is not None:
                module_parts = obj.__module__.split('.')
                module = '.'.join(module_parts[:3])
                modules.setdefault(module, 0)
                modules[module] += 1

        print "Modules with > %d objects:" % threshold
        self.dump_modules(modules, threshold)

        if self._previous:
            changes = {}
            for module, value in modules.items():
                changes[module] = value - self._previous.get(module, 0)

            print "Changes since last time:"
            self.dump_modules(changes, 10)

            self._previous.clear()
        
        self._previous.update(modules)
        print ""

    def dump_modules(self, modules, threshold):
        maxlen = max(len(m) for m in modules)
        l = [(value, module) for module, value in modules.items()
             if value > threshold]
        if l:
            l.sort(reverse=True)
            for value, module in l:
                print "%*s %5d" % (maxlen+1, module, value)
        else:
            print "   <None>" 

    
