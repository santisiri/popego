"""
Text Helpers

Provides a set of methods for filtering, formatting and transforming strings.
"""
# Last synced with Rails copy at Revision 6096 on Feb 8th, 2007.
# Purposely left out sanitize and strip_tags, should be included at some point likely using
# BeautifulSoup.

import itertools
import re
import textwrap
import warnings
import webhelpers.textile as textile
import webhelpers.markdown as _markdown
from routes import request_config
from webhelpers.rails.tags import content_tag, tag_options

AUTO_LINK_RE = re.compile(r"""
                        (                          # leading text
                          <\w+.*?>|                # leading HTML tag, or
                          [^=!:'"/]|               # leading punctuation, or 
                          ^                        # beginning of line
                        )
                        (
                          (?:https?://)|           # protocol spec, or
                          (?:www\.)                # www.*
                        ) 
                        (
                          [-\w]+                   # subdomain or domain
                          (?:\.[-\w]+)*            # remaining subdomains or domain
                          (?::\d+)?                # port
                          (?:/(?:(?:[~\w\+%-]|(?:[,.;:][^\s$]))+)?)* # path
                          (?:\?[\w\+%&=.;-]+)?     # query string
                          (?:\#[\w\-]*)?           # trailing anchor
                        )
                        ([\.,"'?!;:]|\s|<|$)       # trailing text
                           """, re.X)
    
def iterdict(items):
    return dict(items=items, iter=itertools.cycle(items))

def cycle(*args, **kargs):
    """
    Returns the next cycle of the given list
    
    Everytime ``cycle`` is called, the value returned will be the next item
    in the list passed to it. This list is reset on every request, but can
    also be reset by calling ``reset_cycle()``.
    
    You may specify the list as either arguments, or as a single list argument.
    
    This can be used to alternate classes for table rows::
    
        # In Myghty...
        % for item in items:
        <tr class="<% cycle("even", "odd") %>">
            ... use item ...
        </tr>
        % #endfor
    
    You can use named cycles to prevent clashes in nested loops. You'll
    have to reset the inner cycle, manually::
    
        % for item in items:
        <tr class="<% cycle("even", "odd", name="row_class") %>
            <td>
        %     for value in item.values:
                <span style="color:'<% cycle("red", "green", "blue",
                                             name="colors") %>'">
                            item
                </span>
        %     #endfor
            <% reset_cycle("colors") %>
            </td>
        </tr>
        % #endfor
    """
    if len(args) > 1:
        items = args
    else:
        items = args[0]
    name = kargs.get('name', 'default')
    cycles = request_config().environ.setdefault('railshelpers.cycles', {})
    
    cycle = cycles.setdefault(name, iterdict(items))
    
    if cycles[name].get('items') != items:
        cycle = cycles[name] = iterdict(items)
    return cycle['iter'].next()

def reset_cycle(name='default'):
    """
    Resets a cycle
    
    Resets the cycle so that it starts from the first element in the array
    the next time it is used.
    """
    try:
        del request_config().environ['railshelpers.cycles'][name]
    except KeyError:
        pass

def counter(name='default', start=1, step=1):
    """Return the next cardinal in a sequence.

    Every time ``counter`` is called, the value returned will be the next
    counting number in that sequence.  This is reset to ``start`` on every
    request, but can also be reset by calling ``reset_counter()``.

    You can optionally specify the number you want to start at by passing
    in the ``start`` argument (defaults to 1).

    You can also optionally specify the step size you want by passing in
    the ``step`` argument (defaults to 1).

    Sequences will increase monotonically by ``step`` each time it is
    called, until the heat death of the universe or python explodes.

    This can be used to count rows in a table::

        # In Myghty
        % for item in items:
        <tr>
            <td><% h.counter() %></td>
        </tr>
        % #endfor

    You can use named counters to prevent clashes in nested loops.
    You'll have to reset the inner cycle manually though.  See the
    documentation for ``webhelpers.text.cycle()`` for a similar
    example.
    """
    counters = request_config().environ.setdefault('railshelpers.counters', {})

    # ripped off of itertools.count
    def do_counter(start, step):
        while True:
            yield start
            start += step
            
    counter = counters.setdefault(name, do_counter(start, step))

    return counter.next()

def reset_counter(name='default'):
    """Resets a counter.

    Resets the counter so that it starts from the ``start`` cardinal in
    the sequence next time it is used.
    """
    try:
        del request_config().environ['railshelpers.counters'][name]
    except KeyError:
        pass

def truncate(text, length=30, truncate_string='...'):
    """
    Truncates ``text`` with replacement characters
    
    ``length``
        The maximum length of ``text`` before replacement
    ``truncate_string``
        If ``text`` exceeds the ``length``, this string will replace
        the end of the string

    Example::

        >>> truncate('Once upon a time in a world far far away', 14)
        'Once upon a...'
    """
    if not text: return ''
    
    new_len = length-len(truncate_string)
    if len(text) > length:
        return text[:new_len] + truncate_string
    else:
        return text

def highlight(text, phrase, highlighter='<strong class="highlight">\\1</strong>',
              hilighter=None):
    """
    Highlights the ``phrase`` where it is found in the ``text``
    
    The highlighted phrase will be surrounded by the highlighter, by default::
    
        <strong class="highlight">I'm a highlight phrase</strong>
    
    ``highlighter``
        Defines the highlighting phrase. This argument should be a single-quoted string
        with ``\\1`` where the phrase is supposed to be inserted.
        
    Note: The ``phrase`` is sanitized to include only letters, digits, and spaces before use.

    Example::

        >>> highlight('You searched for: Pylons', 'Pylons')
        'You searched for: <strong class="highlight">Pylons</strong>'
    """
    if hilighter is not None:
        warnings.warn("The highlight function's hilight keyword argument is deprecated: "
                      "Please use the highlight keyword argument instead.",
                      DeprecationWarning, 2)
        highlighter = hilighter
    if not phrase or not text:
        return text
    highlight_re = re.compile('(%s)' % re.escape(phrase), re.I)
    return highlight_re.sub(highlighter, text)

def excerpt(text, phrase, radius=100, excerpt_string="..."):
    """
    Extracts an excerpt from the ``text``. Returns an empty string if the phrase
    isn't found.

    ``phrase``
        Phrase to excerpt from ``text``
    ``radius``
        How many surrounding characters to include
    ``excerpt_string``
        Characters surrounding entire excerpt
    
    Example::
    
        >>> excerpt("hello my world", "my", 3)
        '...lo my wo...'
    """
    if not text or not phrase:
        return text

    pat = re.compile('(.{0,%s}%s.{0,%s})' % (radius, re.escape(phrase), radius), re.I)
    match = pat.search(text)
    if not match:
        return ""
    excerpt = match.expand(r'\1')
    if match.start(1) > 0:
        excerpt = excerpt_string + excerpt
    if match.end(1) < len(text):
        excerpt = excerpt + excerpt_string
    return excerpt

def word_wrap(text, line_width=80):
    """
    Wraps ``text`` into lines no longer than ``line_width`` width. This function
    breaks on the first whitespace character that does not exceed ``line_width``.

    Deprecated: Use python's builtin textwrap.fill instead.
    """
    warnings.warn("The word_wrap function has been deprecated: Use python's builtin "
                  "textwrap.fill function instead.", DeprecationWarning, 2)
    return textwrap.fill(text, line_width)

def simple_format(text):
    """
    Returns ``text`` transformed into HTML using very simple formatting rules
    
    Two or more consecutive newlines(``\\n\\n``) are considered as a paragraph
    and wrapped in ``<p>`` tags. One newline (``\\n``) is considered a
    linebreak and a ``<br />`` tag is appended. This method does not remove the
    newlines from the text.
    """
    if text is None:
        text = ''
    text = re.sub(r'(\r\n|\n|\r)', r'\n', text)
    text = re.sub(r'\n\n+', r'\n\n', text)
    text = re.sub(r'(\n\n)', r'</p>\1<p>', text)
    text = re.sub(r'([^\n])(\n)(?=[^\n])', r'\1\2<br />', text)
    text = content_tag("p", text).replace('</p><p></p>', '</p>')
    text = re.sub(r'</p><p>', r'</p>\n<p>', text)
    return text

def auto_link(text, link="all", **href_options):
    """
    Turns all urls and email addresses into clickable links.
    
    ``link``
        Used to determine what to link. Options are "all", "email_addresses", or "urls"
    
    Example::
    
        >>> auto_link("Go to http://www.planetpython.com and say hello to guido@python.org")
        'Go to <a href="http://www.planetpython.com">http://www.planetpython.com</a> and say hello to <a href="mailto:guido@python.org">guido@python.org</a>'
    """
    if not text:
        return ""
    if link == "all":
        return auto_link_urls(auto_link_email_addresses(text), **href_options)
    elif link == "email_addresses":
        return auto_link_email_addresses(text)
    else:
        return auto_link_urls(text, **href_options)

def auto_link_urls(text, **href_options):
    extra_options = tag_options(**href_options)
    def handle_match(matchobj):
        all = matchobj.group()
        a, b, c, d = matchobj.group(1, 2, 3, 4)
        if re.match(r'<a\s', a, re.I):
            return all
        text = b + c
        if b == "www.":
            b = "http://www."
        return '%s<a href="%s%s"%s>%s</a>%s' % (a, b, c, extra_options, text, d)
    return re.sub(AUTO_LINK_RE, handle_match, text)

def auto_link_email_addresses(text):
    return re.sub(r'([\w\.!#\$%\-+.]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+)',
                  r'<a href="mailto:\1">\1</a>', text)

def strip_links(text):
    """
    Strips link tags from ``text`` leaving just the link label.
    
    Example::
    
        >>> strip_links('<a href="something">else</a>')
        'else'
    """
    strip_re = re.compile(r'<a\b.*?>(.*?)<\/a>', re.I | re.M)
    return strip_re.sub(r'\1', text)

def textilize(text, sanitize=False):
    """Format the text with Textile formatting
    
    This function uses the `PyTextile library <http://dealmeida.net/>`_ which is included with WebHelpers.
    
    Additionally, the output can be sanitized which will fix tags like <img />,
    <br /> and <hr /> for proper XHTML output.
    
    """
    texer = textile.Textiler(text)
    return texer.process(sanitize=sanitize)

def markdown(text, **kwargs):
    """Format the text with MarkDown formatting
    
    This function uses the `Python MarkDown library <http://www.freewisdom.org/projects/python-markdown/>`_
    which is included with WebHelpers.
    
    """
    return _markdown.markdown(text, **kwargs)

__all__ = ['cycle', 'reset_cycle', 'counter', 'reset_counter', 'truncate', 'highlight', 'excerpt',
           'word_wrap', 'simple_format', 'auto_link', 'strip_links', 'textilize', 'markdown']
