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

from .forms import AssignMenuForm

# Create your views here.

@staff_member_required
@permission_required('core.manage_settings')
def index(request):
    menus = Menu.objects.all()
    menus = get_paginator_items(menus,request.GET.get('page'))
    print(get_current_site(request))
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
    return TemplateResponse(request, 'dashboard/menu/index.html', ctx)
