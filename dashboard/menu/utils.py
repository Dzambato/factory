from django.db.models import Q
from django.utils.formats import localize
from django.utils.translation import pgettext

from menu.models import Menu, MenuItem
from page.models import Page
from menu.models import Category

def update_menu_item_linked_object(menu_item, linked_object):
    """Assign new linked object to a menu item. Clear other links."""
    menu_item.category = None
    menu_item.page = None

    if isinstance(linked_object, Category):
        menu_item.category = linked_object
    elif isinstance(linked_object, Page):
        menu_item.page = linked_object
    return menu_item.save()

def get_menu_obj_text(obj):
    if getattr(obj, 'is_published', True):
        return str(obj)
    elif isinstance(obj, Page) and obj.is_visible and obj.available_on:
        return pgettext(
            'Menu item page hidden status',
            '%(menu_item_name)s is hidden '
            '(will become visible on %(available_on_date)s)' % ({
                'available_on_date': localize(obj.available_on),
                'menu_item_name': str(obj)}))
    return pgettext(
        'Menu item published status',
        '%(menu_item_name)s (Not published)' % {
            'menu_item_name': str(obj)})




def get_menu_item_as_dict(menu_item):
    data = {}
    if menu_item.linked_object:
        data['url'] = menu_item.linked_object.get_absolute_url()
    else:
        data['url'] = menu_item.url
    data['name'] = menu_item.name
    return data


def get_menu_as_json(menu):
    """Builds Tree-like structure from top menu items,
    its children and its grandchildren.
    """
    top_items = menu.items.filter(
        parent=None).prefetch_related(
            'category', 'page',
            'children__category', 'children__page',
            'children__children__category', 'children__children__page',)
    menu_data = []
    for item in top_items:
        top_item_data = get_menu_item_as_dict(item)
        top_item_data['child_items'] = []
        children = item.children.all()
        for child in children:
            child_data = get_menu_item_as_dict(child)
            grand_children = child.children.all()
            grand_children_data = [
                get_menu_item_as_dict(grand_child)
                for grand_child in grand_children]
            child_data['child_items'] = grand_children_data
            top_item_data['child_items'].append(child_data)
        menu_data.append(top_item_data)
    return menu_data


def update_menu(menu):
    menu.json_content = get_menu_as_json(menu)
    menu.save(update_fields=['json_content'])

def update_menus(menus_pk):
    menus = Menu.objects.filter(pk__in=menus_pk)
    for menu in menus:
        update_menu(menu)


def get_menus_that_needs_update(categories=None, page=None):
    """Returns PrimaryKeys of Menu instances that will be affected by
    deleting one of the listed objects, therefore needs to be updated
    afterwards.
    """
    if not any([page, categories]):
        return []
    q = Q()
    if categories is not None:
        q |= Q(category__in=categories)
    if page is not None:
        q |= Q(page=page)
    menus_to_be_updated = MenuItem.objects.filter(q).distinct().values_list(
        'menu', flat=True)
    return menus_to_be_updated

