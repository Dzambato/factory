from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import permission_required
from ..views import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from menu.models import Menu
from core.utils import get_paginator_items
from django.contrib import messages
from django.utils.translation import pgettext_lazy

from .forms import AssignMenuForm, MenuForm

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
    print(menu.pk)
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
