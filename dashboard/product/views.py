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
from .forms import ProductTypeForm, AttributeForm, AttributeValueForm
from product.models import ProductType, Attribute, AttributeValue


@staff_member_required
@permission_required('product.manage_products')
def product_type_list(request):
    types = ProductType.objects.all().prefetch_related(
        'product_attributes').order_by('name')
    product_types = [
        (pt.pk, pt.name, pt.product_attributes.all()) for pt in types]
    ctx = {
        'product_types': product_types}
    return TemplateResponse(
        request,
        'dashboard/product/product_type/list.html',
        ctx)\


@staff_member_required
@permission_required('product.manage_products')
def product_type_create(request):
    product_type = ProductType()
    form = ProductTypeForm(request.POST or None, instance=product_type)
    if form.is_valid():
        product_type = form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Added product type %s') % (product_type,)
        messages.success(request, msg)
        return redirect('dashboard:product-type-list')
    ctx = {'form': form, 'product_type': product_type}
    return TemplateResponse(
        request,
        'dashboard/product/product_type/form.html',
        ctx)


@staff_member_required
@permission_required('product.manage_products')
def product_type_edit(request, pk):
    product_type = get_object_or_404(ProductType, pk=pk)
    form = ProductTypeForm(request.POST or None, instance=product_type)
    if form.is_valid():
        product_type = form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated product type %s') % (product_type,)
        messages.success(request, msg)
        return redirect('dashboard:product-type-update', pk=pk)
    ctx = {'form': form, 'product_type': product_type}
    return TemplateResponse(
        request,
        'dashboard/product/product_type/form.html',
        ctx)




@staff_member_required
@permission_required('product.manage_products')
def product_type_delete(request, pk):
    product_type = get_object_or_404(ProductType, pk=pk)
    if request.method == 'POST':
        product_type.delete()
        msg = pgettext_lazy(
            'Dashboard message', 'Removed product type %s') % (product_type,)
        messages.success(request, msg)
        return redirect('dashboard:product-type-list')
    ctx = {
        'product_type': product_type,
        'products': product_type.products.all()}
    return TemplateResponse(
        request,
        'dashboard/product/product_type/modal/confirm_delete.html',
        ctx)

@staff_member_required
@permission_required('product.manage_products')
def attribute_list(request):
    raw_attributes = (
        Attribute.objects.prefetch_related(
            'values', 'product_type').order_by('name'))
    attributes = [(
        attribute.pk,
        attribute.name,
        attribute.product_type,
        attribute.values.all()) for attribute in raw_attributes]

    ctx = {
        'attributes': attributes,
    }
    return TemplateResponse(
        request, 'dashboard/product/attribute/list.html', ctx)


















@staff_member_required
@permission_required('product.manage_products')
def attribute_details(request, pk):
    attributes = Attribute.objects.prefetch_related(
        'values', 'product_type',).all()
    attribute = get_object_or_404(attributes, pk=pk)
    product_type = attribute.product_type
    values = attribute.values.all()
    ctx = {
        'attribute': attribute, 'product_type': product_type, 'values': values}
    return TemplateResponse(
        request, 'dashboard/product/attribute/detail.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def attribute_create(request):
    attribute = Attribute()
    form = AttributeForm(request.POST or None, instance=attribute)
    if form.is_valid():
        attribute = form.save()
        msg = pgettext_lazy('Dashboard message', 'Added attribute')
        messages.success(request, msg)
        return redirect('dashboard:attribute-details', pk=attribute.pk)
    ctx = {'attribute': attribute, 'form': form}
    return TemplateResponse(
        request, 'dashboard/product/attribute/form.html', ctx)





@staff_member_required
@permission_required('product.manage_products')
def attribute_edit(request, pk):
    raw_attributes = (
        Attribute.objects.prefetch_related(
            'values', 'product_type').order_by('name'))
    attributes = [(
        attribute.pk,
        attribute.name,
        attribute.product_type,
        attribute.values.all()) for attribute in raw_attributes]

    ctx = {
        'attributes': attributes,
    }
    return TemplateResponse(
        request, 'dashboard/product/attribute/list.html', ctx)





@staff_member_required
@permission_required('product.manage_products')
def attribute_delete(request, pk):
    raw_attributes = (
        Attribute.objects.prefetch_related(
            'values', 'product_type').order_by('name'))
    attributes = [(
        attribute.pk,
        attribute.name,
        attribute.product_type,
        attribute.values.all()) for attribute in raw_attributes]

    ctx = {
        'attributes': attributes,
    }
    return TemplateResponse(
        request, 'dashboard/product/attribute/list.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def attribute_value_create(request, attribute_pk):
    attribute = get_object_or_404(Attribute, pk=attribute_pk)
    value = AttributeValue(attribute_id=attribute_pk)
    form = AttributeValueForm(request.POST or None, instance=value)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Added attribute\'s value')
        messages.success(request, msg)
        return redirect('dashboard:attribute-details', pk=attribute_pk)
    ctx = {'attribute': attribute, 'value': value, 'form': form}
    return TemplateResponse(
        request,
        'dashboard/product/attribute/values/form.html',
        ctx)




@staff_member_required
@permission_required('product.manage_products')
def attribute_value_edit(request, attribute_pk, value_pk):
    attribute = get_object_or_404(Attribute, pk=attribute_pk)
    value = get_object_or_404(AttributeValue, pk=value_pk)
    form = AttributeValueForm(request.POST or None, instance=value)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated attribute\'s value')
        messages.success(request, msg)
        return redirect('dashboard:attribute-details', pk=attribute_pk)
    ctx = {'attribute': attribute, 'value': value, 'form': form}
    return TemplateResponse(
        request,
        'dashboard/product/attribute/values/form.html',
        ctx)



@staff_member_required
@permission_required('product.manage_products')
def attribute_value_delete(request, attribute_pk, value_pk):
    value = get_object_or_404(AttributeValue, pk=value_pk)
    if request.method == 'POST':
        value.delete()
        msg = pgettext_lazy(
            'Dashboard message',
            'Removed attribute\'s value %s') % (value.name,)
        messages.success(request, msg)
        return redirect('dashboard:attribute-details', pk=attribute_pk)
    return TemplateResponse(
        request,
        'dashboard/product/attribute/values/modal/confirm_delete.html',
        {'value': value, 'attribute_pk': attribute_pk})

@staff_member_required
@permission_required('product.manage_products')
def ajax_reorder_attribute_values(request, attribute_pk):
    raw_attributes = (
        Attribute.objects.prefetch_related(
            'values', 'product_type').order_by('name'))
    attributes = [(
        attribute.pk,
        attribute.name,
        attribute.product_type,
        attribute.values.all()) for attribute in raw_attributes]

    ctx = {
        'attributes': attributes,
    }
    return TemplateResponse(
        request, 'dashboard/product/attribute/list.html', ctx)


