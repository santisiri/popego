"""Pagination Link Generators"""
from webhelpers.htmlgen import html

def pagelist(page):
    """PHPbb style Pagination Links
    
    This returns HTML source to be included into a page. The html is generated
    with htmlgen
    """
    paginator = page.paginator

    first_page = paginator[0]
    first_window = first_page.window(padding=3)

    page_window = page.window(padding=1)

    last_page = paginator[-1]
    last_window = last_page.window(padding=3)

    first_past_page = first_window.last >= page_window.first
    page_past_last = page_window.last >= last_window.first

    def combine_pages(page_list):
        seen = {}
        result = []
        for page in page_list:
            if page in seen: continue
            seen[page] = 1
            result.append(page)
        return result

    if first_past_page:
        if page_past_last:
            display = first_window.pages
        else:
            first_window.last = page_window.last
            display = (first_window.pages + [None] + last_window.pages)
    else:
        if page_past_last:
            page_window.last = last_window.last
            display = (first_window.pages + [None] + page_window.pages)
        else:
            display = (first_window.pages + [None] + page_window.pages + [None]
                    + last_window.pages)

    pager_c = []
    for i in display:
        if i is None:
            pager_c.append(html.span(c='...'))
        elif i == page:
            pager_c.append(html.span(c=[i]))
        else:
            pager_c.append(html.a(href=i, c=[i]))

    pager = html.div(class_='pager', c=pager_c)

    return pager
