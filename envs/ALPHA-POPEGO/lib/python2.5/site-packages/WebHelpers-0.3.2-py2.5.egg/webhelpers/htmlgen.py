"""
htmlgen

Kind of like HTMLGen, only much simpler.  Like stan, only not.  The
only important symbol that is exported is ``html``.

You create tags with attribute access.  I.e., the ``A`` anchor tag is
``html.a``.  The attributes of the HTML tag are done with keyword
arguments.  The contents of the tag are the non-keyword arguments
(concatenated).  You can also use the special ``c`` keyword, passing a
list, tuple, or single tag, and it will make up the contents (this is
useful because keywords have to come after all non-keyword arguments,
which is non-intuitive).

If the value of an attribute is None, then no attribute will be
inserted.  So::

    >>> html.a(href='http://www.yahoo.com', name=None, c='Click Here')
    '<a href=\"http://www.yahoo.com\">Click Here</a>'

If a non-string is passed in, then ``webhelpers.escapes.html_escape``
is called on the value.

``html`` can also be called, and it will concatenate the string
representations of its arguments.

``html.comment`` will generate an HTML comment, like
``html.comment('comment text', 'and some more text')`` -- note that it
cannot take keyword arguments (because they wouldn't mean anything).

For cases where you cannot use a name (e.g., for the ``class``
attribute) you can append an underscore to the name, like
``html.span(class_='alert')``.

Examples::

    >>> html.html(
    ...    html.head(html.title(\"Page Title\")),
    ...    html.body(
    ...    bgcolor='#000066',
    ...    text='#ffffff',
    ...    c=[html.h1('Page Title'),
    ...       html.p('Hello world!')],
    ...    ))
    '<html><head><title>Page Title</title></head><body text="#ffffff" bgcolor="#000066"><h1>Page Title</h1><p>Hello world!</p></body></html>'
    >>> html.a(href='#top', c='return to top')
    '<a href=\"#top\">return to top</a>'

.. note::

   Should this return objects instead of strings?  That would allow
   things like ``html.a(href='foo')('title')``.  Also, the objects
   could have a method that shows that they are trully HTML, and thus
   should not be further quoted.

   However, in some contexts you can't use objects, you need actual
   strings.  But maybe we can just make sure those contexts don't
   happen in webhelpers.
"""

from util import html_escape

__all__ = ['html']

def strify(s):
    if s is None:
        return ''
    if not isinstance(s, basestring):
        s = unicode(s)
    if isinstance(s, unicode):
        s = s.encode('ascii', 'xmlcharrefreplace')
    return s

class UnfinishedComment:

    def __call__(self, *args):
        return '<!--%s-->' % '\n'.join(map(strify, args))

class Base:

    comment = UnfinishedComment()

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError
        attr = attr.lower()
        return UnfinishedTag(attr)

    def __call__(self, *args):
        return ''.join(map(str, args))

    def escape(self, *args):
        return ''.join(map(html_escape, args))

    def str(self, arg):
        return strify(arg)

class UnfinishedTag:

    def __init__(self, tag):
        self._tag = tag

    def __call__(self, *args, **kw):
        return tag(self._tag, *args, **kw)

    def __str__(self):
        if self._tag in empty_tags:
            return '<%s />' % self._tag
        else:
            return '<%s></%s>' % (self._tag, self._tag)

def tag(tag, *args, **kw):
    if kw.has_key("c"):
        if args:
            raise TypeError(
                "The special 'c' keyword argument cannot be used in "
                "conjunction with non-keyword arguments")
        args = kw["c"]
        del kw["c"]
    attrargs = []
    for attr, value in kw.items():
        if value is None:
            continue
        if attr.endswith('_'):
            attr = attr[:-1]
        attrargs.append(' %s="%s"' % (attr, html_escape(value)))
    if not args and tag in empty_tags:
        return '<%s%s />' % (tag, ''.join(attrargs))
    else:
        return '<%s%s>%s</%s>' % (
            tag, ''.join(attrargs), ''.join(map(strify, args)),
            tag)

# Taken from: http://www.w3.org/TR/REC-html40/index/elements.html
empty_tags = {}
for _t in ("area base basefont br col frame hr img input isindex "
           "link meta param".split()):
    empty_tags[_t] = None

block_level_tags = {}
for _t in ("applet blockquote body br dd div dl dt fieldset "
           "form frameset head hr html iframe map menu noframes "
           "noscript object ol optgroup p param script select "
           "table tbody tfoot thead tr ul var"):
    block_level_tags[_t] = None

html = Base()

