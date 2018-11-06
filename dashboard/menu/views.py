from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import permission_required
from ..views import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from menu.models import Menu, MenuItem
from core.utils import get_paginator_items
from dashboard.menu.utils import get_menu_obj_text, update_menu
from django.contrib import messages
from django.utils.translation import pgettext_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .forms import AssignMenuForm, MenuForm, MenuItemForm

from page.models import Page
from menu.models import Category

# Create your views here.

@staff_member_required
@permission_required('core.manage_settings')
def index(request):
    menus = Menu.objects.all()
    menus = get_paginator_items(menus,request.GET.get('page'))
    site_settings = get_current_site(request).settings
    assign_menu_form = AssignMenuForm(request.POST or None,instance=site_settings)
    if request.POST and assign_menu_form.is_valid():
        assign_menu_form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated storefront menus')
        messages.success(request, msg)
        return redirect('dashboard:menu-index')
    ctx = {
        'menus' : menus,
        'assign_menu_form' : assign_menu_form,
        'site_settings' : site_settings,
    }
    return TemplateResponse(request, 'dashboard/menu/index.html', ctx)\



@staff_member_required
@permission_required('core.manage_settings')
def menu_details(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu_items = menu.items.filter(parent=None).prefetch_related(
        'category', 'page')

    ctx = {
        'menu': menu,
        'menu_items': menu_items,
    }
    return TemplateResponse(request, 'dashboard/menu/details.html', ctx)\


@staff_member_required
@permission_required('core.manage_settings')
def menu_item_details (request, menu_pk, item_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    menu_item = menu.items.get(pk=item_pk)

    menu_items = menu_item.get_children().order_by('sort_order')

    ctx = {
        'menu': menu,
        'menu_items': menu_items,
        'menu_item': menu_item,
    }
    return TemplateResponse(request, 'dashboard/menu/item/details.html', ctx)


@staff_member_required
@permission_required('core.manage_settings')
def menu_create (request):
    menu = Menu()
    menu_form = MenuForm(request.POST, instance=menu)
    if menu_form.is_valid() and menu_form.has_changed() and request.POST:
        menu = menu_form.save()
        msg = pgettext_lazy('Dashboard message', 'Added menu %s') % (menu,)
        messages.success(request, msg)
        return redirect('dashboard:menu-index')
    ctx = {
        'form': menu_form,
        'menu': menu
    }
    return TemplateResponse(request, 'dashboard/menu/form.html', ctx)



@staff_member_required
@permission_required('menu.manage_menus')
def menu_edit(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu_form = MenuForm(request.POST or None, instance=menu)
    if menu_form.is_valid() and menu_form.has_changed() and request.POST:
        menu = menu_form.save()
        msg = pgettext_lazy('Dashboard message', 'Updated menu %s') % (menu,)
        messages.success(request, msg)
        return redirect('dashboard:menu-details', pk=menu.pk)
    ctx = {
        'form': menu_form,
        'menu': menu
    }

    return TemplateResponse(request, 'dashboard/menu/form.html', ctx)



@staff_member_required
@permission_required('menu.manage_menus')
def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu.delete()
        msg = pgettext_lazy('Dashboard message', 'Removed menu %s') % (menu,)
        messages.success(request, msg)
        return redirect('dashboard:menu-list')
    ctx = {
        'menu': menu, 'descendants': list(menu.items.all())}
    return TemplateResponse(
        request, 'dashboard/menu/modal/confirm_delete.html', ctx)



@staff_member_required
@permission_required('menu.manage_menus')
def ajax_menu_links(request):

    def get_obj_repr(obj):
        obj_id = str(obj.pk) + '_' + obj.__class__.__name__
        return {
            'id': obj_id,
            'text': get_menu_obj_text(obj)}

    def get_group_repr(model, label, filter_fields, query):
        queryset = model.objects.all()
        if search_query and search_query.lower() not in label.lower():
            kwargs = {
                '%s__contains' % (field,): query for field in filter_fields}
            queryset = queryset.filter(Q(**kwargs))
        return {
            'text': label,
            'children': [get_obj_repr(obj) for obj in queryset]}

    search_query = request.GET.get('q', '')
    groups = [
        get_group_repr(
            Category,
            pgettext_lazy('Link object type group description', 'Category'),
            ('name',),
            search_query),
        get_group_repr(
            Page,
            pgettext_lazy('Link object type group description', 'Page'),
            ('title',),
            search_query)
    ]

    groups = [group for group in groups if len(group.get('children')) > 0]
    return JsonResponse({'results': groups})



@staff_member_required
@permission_required('menu.manage_menus')
def menu_item_create(request, menu_pk, root_pk=None):
    menu = get_object_or_404(Menu, pk=menu_pk)
    path = None
    if root_pk:
        root = get_object_or_404(MenuItem, pk=root_pk)
        path = root.get_ancestors(include_self=True)
        menu_item = MenuItem(menu=menu, parent=root)
    else:
        menu_item = MenuItem(menu=menu)
    form = MenuItemForm(request.POST or None, instance=menu_item)
    if form.is_valid():
        menu_item = form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Added menu item %s') % (menu_item,)
        messages.success(request, msg)
        update_menu(menu)
        if root_pk:
            return redirect(
                'dashboard:menu-item-details',
                menu_pk=menu.pk, item_pk=root_pk)
        return redirect('dashboard:menu-details', pk=menu.pk)
    ctx = {
        'form': form, 'menu': menu, 'menu_item': menu_item, 'path': path}
    return TemplateResponse(request, 'dashboard/menu/item/form.html', ctx)

@staff_member_required
@permission_required('menu.manage_menus')
def menu_item_delete(request, menu_pk, item_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    menu_item = get_object_or_404(menu.items.all(), pk=item_pk)
    if request.method == 'POST':
        menu_item.delete()
        update_menu(menu)
        msg = pgettext_lazy(
            'Dashboard message', 'Removed menu item %s') % (menu_item,)
        messages.success(request, msg)
        root_pk = menu_item.parent.pk if menu_item.parent else None
        if root_pk:
            redirect_url = reverse(
                'dashboard:menu-item-details', kwargs={
                    'menu_pk': menu_item.menu.pk, 'item_pk': root_pk})
        else:
            redirect_url = reverse(
                'dashboard:menu-details', kwargs={'pk': menu.pk})
        return (
            JsonResponse({'redirectUrl': redirect_url}) if request.is_ajax()
            else redirect(redirect_url))
    ctx = {
        'menu_item': menu_item,
        'descendants': list(menu_item.get_descendants())}
    return TemplateResponse(
        request, 'dashboard/menu/item/modal/confirm_delete.html', ctx)



@staff_member_required
@permission_required('menu.manage_menus')
def menu_item_edit(request, menu_pk, item_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    menu_item = get_object_or_404(menu.items.all(), pk=item_pk)
    path = menu_item.get_ancestors(include_self=True)
    form = MenuItemForm(request.POST or None, instance=menu_item)
    if form.is_valid():
        menu_item = form.save()
        update_menu(menu)
        msg = pgettext_lazy(
            'Dashboard message', 'Saved menu item %s') % (menu_item,)
        messages.success(request, msg)
        return redirect(
            'dashboard:menu-item-details', menu_pk=menu.pk, item_pk=item_pk)
    ctx = {
        'form': form, 'menu': menu, 'menu_item': menu_item, 'path': path}
    return TemplateResponse(request, 'dashboard/menu/item/form.html', ctx)
