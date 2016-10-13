"""Pagination for Collections and ORMs

The Pagination module aids in the process of paging large collections of
objects. It can be used macro-style for automatic fetching of large collections
using one of the ORM wrappers, or handle a large collection responding to
standard Python list slicing operations. These methods can also be used
individually and customized to do as much or little as desired.

The Paginator itself maintains pagination logic associated with each page, 
where begins, what the first/last item on the page is, etc.

Helper functions hook-up the Paginator in more conveinent methods for the more
macro-style approach to return the Paginator and the slice of the collection
desired.

"""
import re

from routes import request_config
from orm import get_wrapper

find_page = re.compile('page=(\d+)', re.I)

def paginate(collection, page=None, per_page=10, item_count=None, 
             query_args=None, **options):
    """Paginate a collection of data
    
    If the collection is a list, it will return the slice of the list along
    with the Paginator object. If the collection is given using an ORM, the
    collection argument must be a partial representing the function to be
    used that will generate the proper query and extend properly for the
    limit/offset.
    
    query_args will be passed to the partial and is for use in generating
    limiting conditions that your collection object may take, the remaining
    unused keyword arguments will also be passed into the collection object.
    
    Example::
    
        # In this case, Person is a SQLObject class, or it could be a 
        # list/tuple
        person_paginator, person_set = paginate(Person, page=1)
        
        set_count = int(person_paginator.current)
        total_pages = len(person_paginator)
    
    Current ORM support is limited to SQLObject and SQLAlchemy. You can use any
    ORM you'd like with the Paginator as it will give you the offset/limit 
    data necessary to make your own query.
    
    If you fail to pass in a page value, paginate will attempt to find a page
    value in the QUERY_STRING from environ, or the Routes match dict. This 
    feature only works if routes was used to resolve the URL.
    
    Example::
        
        # Using an SQLAlchemy object with assign_mapper under Pylons
        # with an order_by passed in
        c.paginator, c.people = paginate(model.Person,
                                         order_by=[model.Person.c.date])
    
    **WARNING:** Unless you pass in an item_count, a count will be performed 
    on the collection every time paginate is called. If using an ORM, it's 
    suggested that you count the items yourself and/or cache them.
    """
    # If our page wasn't passed in, attempt to pull out either a page arg from
    # the routes route path, or try the environ GET.
    if page is None:
        config = request_config()
        if hasattr(config, 'mapper_dict'):
            page = config.mapper_dict.get('page')
        if page is not None:
            if re.match(r'\d+', page):
                page = int(page)
            else:
                page = 0
        elif page is None and hasattr(config, 'environ'):
            page_match = re.match(find_page, 
                                  config.environ.get('QUERY_STRING', ''))
            if page_match:
                page = int(page_match.groups()[0])
        
        # If environ is set, and no page has been we will assume they wanted to
        # find a page value but didn't so we default to 0 now.
        if page is None:
            page = 0
    
    if query_args is None:
        query_args = []
    
    collection = get_wrapper(collection, *query_args, **options)
    if not item_count:
        item_count = len(collection)
    paginator = Paginator(item_count, per_page, page)
    if page < 0 or page >= len(paginator):
        subset = []
    else:
        subset = collection[paginator.current.first_item:paginator.current.last_item]
    
    return paginator, subset
    
    
class Paginator(object):
    """Tracks paginated sets of data, and supplies common pagination operations
    
    The Paginator tracks data associated with pagination of groups of data, as well
    as supplying objects and methods that make dealing with paginated results easier.
    
    A Paginator supports list operations, including item fetching, length, iteration,
    and the 'in' operation. Each item in the Paginator is a Page object representing
    data about that specific page in the set of paginated data. As with the standard
    Python list, the Paginator list index starts at 0.
    
    """
    def __init__(self, item_count, items_per_page=10, current_page=0):
        """Initialize a Paginator with the item count specified."""
        self.item_count = item_count
        self.items_per_page = items_per_page
        self.pages = {}
        self.current_page = current_page
    
    def current():
        doc = """\
Page object currently being displayed

When assigning to the current page, it will set the page number for this page
and create it if needed. If the page is a Page object and does not belong to
this paginator, an AttributeError will be raised.

"""
        def fget(self):
            return self[int(self.current_page)]
        def fset(self, page):
            if isinstance(page, Page) and page.paginator != self:
                raise AttributeError("Page/Paginator mismatch")
            page = int(page)
            self.current_page = page in self and page or 0
        return locals()
    current = property(**current())
    
    def __len__(self):
        if self.item_count == 0:
            return 0
        else:
            return ((self.item_count - 1)//self.items_per_page) + 1
    
    def __iter__(self):
        for i in range(0, len(self)):
            yield self[i]
    
    def __getitem__(self, index):
        # Handle negative indexing like a normal list
        if index < 0:
            index = len(self) + index
        
        if index < 0:
            index = 0
        
        if index not in self and index != 0:
            raise IndexError, "list index out of range"
        
        return self.pages.setdefault(index, Page(self, index))
    
    def __contains__(self, value):
        if value >= 0 and value <= (len(self) - 1):
            return True
        return False

class Page(object):
    """Represents a single page from a paginated set."""
    def __init__(self, paginator, number):
        """Creates a new Page for the given ``paginator`` with the index ``number``."""
        self.paginator = paginator
        self.number = int(number)
    
    def __int__(self):
        return self.number
    
    def __eq__(self, page):
        return self.paginator == page.paginator and self.number == page.number
    
    def __cmp__(self, page):
        return cmp(self.number, page.number)
    
    def offset():
        doc = """Offset of the page, useful for database queries."""
        def fget(self):
            return self.paginator.items_per_page * self.number
        return locals()
    offset = property(**offset())
    
    def first_item():
        doc = """The number of the first item in the page."""
        def fget(self):
            return self.offset
        return locals()
    first_item = property(**first_item())
    
    def last_item():
        doc = """The number of the last item in the page."""
        def fget(self):
            return min(self.paginator.items_per_page * (self.number + 1),
                self.paginator.item_count)
        return locals()
    last_item = property(**last_item())
    
    def first():
        doc = """Boolean indiciating if this page is the first."""
        def fget(self):
            return self == self.paginator[0]
        return locals()
    first = property(**first())
    
    def last():
        doc = """Boolean indicating if this page is the last."""
        def fget(self):
            return self == self.paginator[-1]
        return locals()
    last = property(**last())
    
    def previous():
        doc = """Previous page if it exists, None otherwise."""
        def fget(self):
            if self.first:
                return None
            return self.paginator[self.number - 1]
        return locals()
    previous = property(**previous())
    
    def next():
        doc = """Next page if it exists, None otherwise."""
        def fget(self):
            if self.last:
                return None
            return self.paginator[self.number + 1]
        return locals()
    next = property(**next())

    def window(self, padding = 2):
        return Window(self, padding)
    
    def __repr__(self):
        return str(self.number)

class Window(object):
    """Represents ranges around a given page."""
    def __init__(self, page, padding = 2):
        """Creates a new Window object for the given ``page`` with the specified ``padding``."""
        self.paginator = page.paginator
        self.page = page
        self.padding = padding
    
    def padding():
        doc = """Sets the window's padding (the number of pages on either side of the window page)."""
        def fset(self, padding):
            self._padding = padding
            if padding < 0: self._padding = 0
            first_page_in_window = self.page.number - self._padding
            self.first = first_page_in_window in self.paginator and (
                self.paginator[first_page_in_window]) or self.paginator[0]
            last_page_in_window = self.page.number + self._padding
            self.last = last_page_in_window in self.paginator and (
                self.paginator[last_page_in_window]) or self.paginator[-1]
        def fget(self):
            return self._padding
        return locals()
    padding = property(**padding())
    
    def pages():
        doc = """Returns a list of Page objects in the current window."""
        def fget(self):
            return [self.paginator[page_number] for page_number in 
                range(self.first.number, self.last.number+1)]
        return locals()
    pages = property(**pages())

    def __add__(self, window):
        if window.paginator != self.paginator:
            raise AttributeError("Window/paginator mismatch")
        assert self.last >= window.first
        return Window(self.page.next, padding=self.padding+1)
