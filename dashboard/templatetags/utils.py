from json import dumps
from urllib.parse import urlencode

from django import forms
from django.template import Library
from django.templatetags.static import static
from versatileimagefield.widgets import VersatileImagePPOIClickWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

register = Library()


@register.inclusion_tag(
    'dashboard/includes/_sorting_header.html', takes_context=True)
def sorting_header(context, field, label, is_wide=False):
    """Render a table sorting header."""
    request = context['request']
    request_get = request.GET.copy()
    sort_by = request_get.get('sort_by')

    # path to icon indicating applied sorting
    sorting_icon = ''

    # flag which determines if active sorting is on field
    is_active = False

    if sort_by:
        if field == sort_by:
            is_active = True
            # enable ascending sort
            # new_sort_by is used to construct a link with already toggled
            # sort_by value
            new_sort_by = '-%s' % field
            sorting_icon = static('images/arrow-up-icon.svg')
        else:
            # enable descending sort
            new_sort_by = field
            if field == sort_by.strip('-'):
                is_active = True
                sorting_icon = static('images/arrow-down-icon.svg')
    else:
        new_sort_by = field

    request_get['sort_by'] = new_sort_by
    return {
        'url': '%s?%s' % (request.path, request_get.urlencode()),
        'is_active': is_active, 'sorting_icon': sorting_icon, 'label': label,
        'is_wide': is_wide}


@register.filter
def is_versatile_image_ppoi_click_widget(field):
    """Check if image field widget is used when editing a product image."""
    return isinstance(field.field.widget, VersatileImagePPOIClickWidget)


# @register.filter
# def is_image_preview_widget(field):
#     """Check if image field widget is used when adding a product image."""
#     return isinstance(field.field.widget, ImagePreviewWidget)

@register.filter
def is_ckeditor(field):
    return isinstance(field.field.widget, CKEditorUploadingWidget)