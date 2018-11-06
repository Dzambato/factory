from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import permission_required
from ..views import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from menu.models import Menu, MenuItem
from core.utils import get_paginator_items
from dashboard.menu.utils import update_menus, update_menu,get_menus_that_needs_update
from django.contrib import messages
from django.utils.translation import pgettext_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse

from page.models import Page
from .forms import PageForm
from menu.models import Category


@staff_member_required
@permission_required('page.manage_pages')
def page_list(request):
    pages = Page.objects.all()

    ctx = {
        'pages': pages,
    }
    return TemplateResponse(request, 'dashboard/page/list.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_add(request):
    page = Page()
    form = PageForm(request.POST or None, instance=page)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy('Dashboard message', 'Saved page')
        messages.success(request, msg)
        return redirect('dashboard:page-details', pk=page.pk)
    ctx = {
        'page': page, 'form': form}
    return TemplateResponse(request, 'dashboard/page/form.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_details(request, pk):
    page = get_object_or_404(Page, pk=pk)
    ctx = {
        'page': page,
    }
    return TemplateResponse(request, 'dashboard/page/detail.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_update(request, pk):
    page = get_object_or_404(Page, pk=pk)
    form = PageForm(request.POST or None, instance=page)
    if form.is_valid() and form.has_changed():
        form.save()
        msg = pgettext_lazy('Dashboard message', 'Saved page')
        messages.success(request, msg)
        return redirect('dashboard:page-details', pk=page.pk)
    ctx = {
        'page': page, 'form': form}
    return TemplateResponse(request, 'dashboard/page/form.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.POST:
        menus = get_menus_that_needs_update(page=page)
        page.delete()
        if menus:
            update_menus(menus)
        msg = pgettext_lazy(
            'Dashboard message', 'Removed page %s') % (page.title,)
        messages.success(request, msg)
        return redirect('dashboard:page-list')
    ctx = {'page': page}
    return TemplateResponse(request, 'dashboard/page/modal_delete.html', ctx)

