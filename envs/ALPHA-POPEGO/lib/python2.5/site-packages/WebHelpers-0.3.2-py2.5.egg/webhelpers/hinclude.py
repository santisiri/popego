"""
``Tired of regenerating HTML pages from templates? Want more from Web caches?
HInclude makes one thing very easy; including other bits of HTML into your Web
page, using the browser.``

http://www.mnot.net/javascript/hinclude.html
"""

from webhelpers.util import html_escape
from webhelpers.rails.tags import content_tag

def include(url, default=''):
    """Do a client-side include of ``url``, defaulting to ``default```
        >>> include("/foo","hello")
        '<hx:include src="/foo">hello</hx:include>'
    """
    
    if callable(url):
        url = url()
    else:
        url = html_escape(url)

    return content_tag("hx:include", content=default, src=url)
