def mapDict(f, a):
    newDict = {}
    for k in a.keys():
        newDict[k] = f(a[k])
    return newDict

def izipDictWith(f, keys, a, b):
    for k in keys:
        yield f(k, a[k], b[k])

def findFirst(predicate, iterable):
    for i in iterable:
        if predicate(i):
            return i
    return None

def all(predicate, iterable):
    for i in iterable:
        if not predicate(i):
            return False
    return True

def concat(iterable):
    for aList in iterable:
        for e in aList:
            yield e
