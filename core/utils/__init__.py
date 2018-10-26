from django.core.paginator import InvalidPage, Paginator
from django.conf import settings
from django.http import Http404

def get_paginator_items(items,page_number):
        paginator = Paginator(items, settings.DASHBOARD_PAGINATE_BY)
        if not page_number:
            page_number = 1
        try:
            page_number = int(page_number)
        except ValueError:
            raise Http404('Page can not be converted to an int.')

        try:
            items = paginator.page(page_number)
        except InvalidPage as err:
            raise Http404('Invalid page (%(page_number)s): %(message)s' % {
                'page_number': page_number, 'message': str(err)})
        return items
