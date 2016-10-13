"""ORM Wrappers"""
import inspect
from webhelpers.util import Partial

orms = {}
try:
    import sqlobject
except:
    pass
else:
    orms['sqlobject'] = True
try:
    import sqlalchemy
except:
    pass
else:
    orms['sqlalchemy'] = True

def get_wrapper(obj, *args, **kw):
    if isinstance(obj, (list, tuple)):
        return obj
    if orms.get('sqlobject'):
        if inspect.isclass(obj) and issubclass(obj, sqlobject.SQLObject):
            return SQLObjectLazy(obj.select, *args, **kw)
    if orms.get('sqlalchemy'):
        if hasattr(obj, '_is_primary_mapper') or \
           (not sqlalchemy.__version__.startswith('0.4') and \
            isinstance(obj, sqlalchemy.Query)):
            return SQLAlchemyLazyMapper(obj, *args, **kw)
        if hasattr(obj, 'mapper') and hasattr(obj, 'select') and hasattr(obj, 'count'):
            return SQLAlchemyLazyMapper(obj, *args, **kw)
        if isinstance(obj, sqlalchemy.Table):
            return SQLAlchemyLazyTable(obj, *args, **kw)
        if hasattr(obj, 'query'):
            return SQLAlchemy04LazySessionMapper(obj, *args, **kw)
        if '_session' in kw:
            return SQLAlchemy04LazyMapper(obj, *args, **kw)
    raise TypeError("You must call paginate() with either a sequence, an "
                    "SQLObject class or an SQLAlchemy query object.")
    

class SQLObjectLazy(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLObjectLazy doesn't support getitem without slicing"
        return list(self()[key.start:key.stop])
    
    def __len__(self):
        return self().count()

class SQLAlchemyLazyTable(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLAlchemyLazy doesn't support getitem without slicing"
        limit = key.stop - key.start
        offset = key.start
        fn = self.fn
        self.fn = fn.select
        results = self(limit=limit, offset=offset).execute()
        self.fn = fn
        return results
    
    def __len__(self):
        s = self.fn.select(*self.args, **self.kw)
        return self.fn([func.count(1)], from_obj=[s])

class SQLAlchemyLazyMapper(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLAlchemyLazy doesn't support getitem without slicing"
        limit = key.stop - key.start
        offset = key.start
        fn = self.fn
        self.fn = fn.select
        results = self(limit=limit, offset=offset)
        self.fn = fn
        return results
    
    def __len__(self):
        kw = {}
        for k, v in self.kw.iteritems():
            if k != 'order_by':
                kw[k] = v
        return self.fn.count(*self.args, **kw)

class SQLAlchemy04LazySessionMapper(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLAlchemyLazy doesn't support getitem without slicing"
        limit = key.stop - key.start
        offset = key.start
        fn = self.fn
        result = fn.query
        if self.args:
            result = result.filter(*self.args)
        
        # Translate keyword args like 'order_by=blah' into func calls for SA 0.4
        # such that its .order_by(blah) on the query object
        for key, val in self.kw.iteritems():
            result = getattr(result, key)(val)
        return result.limit(limit).offset(offset).all()
    
    def __len__(self):
        kw = {}
        fn = self.fn.query
        if self.args:
            fn = fn.filter(*self.args)
        
        for key, val in self.kw.iteritems():
            fn = getattr(fn, key)(val)
        return fn.count()

class SQLAlchemy04LazyMapper(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLAlchemyLazy doesn't support getitem without slicing"
        Session = self.kw.pop('_session')
        limit = key.stop - key.start
        offset = key.start
        fn = self.fn
        result = Session.query(fn)
        if self.args:
            result = result.filter(*self.args)
        
        # Translate keyword args like 'order_by=blah' into func calls for SA 0.4
        # such that its .order_by(blah) on the query object
        for key, val in self.kw.iteritems():
            result = getattr(result, key)(val)
        query = result.limit(limit).offset(offset)
        self.kw['_session'] = Session
        return query.all()
    
    def __len__(self):
        Session = self.kw.pop('_session')
        kw = {}
        fn = Session.query(self.fn)
        if self.args:
            fn = fn.filter(*self.args)
        
        for key, val in self.kw.iteritems():
            fn = getattr(fn, key)(val)
        count = fn.count()
        self.kw['_session'] = Session
        return count
