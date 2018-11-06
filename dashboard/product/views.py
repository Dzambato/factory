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
from .forms import ProductTypeForm, AttributeForm, AttributeValueForm, ProductBulkUpdate, Attribute, AttributeValue, ProductTypeSelectorForm, ProductForm, ProductImageForm
from product.models import ProductType, Product, ProductImage


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






















@staff_member_required
@permission_required('product.manage_products')
def product_list(request):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)


@staff_member_required
@permission_required('product.manage_products')
def product_bulk_update(request):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def ajax_products_list(request):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def product_delete(request, pk):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def product_edit(request, pk):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def product_create(request, type_pk):
    product_type = get_object_or_404(ProductType, pk=type_pk)
    product = Product(product_type=product_type)
    product_form = ProductForm(request.POST or None, instance=product)

    if product_form.is_valid():
        product = product_form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Added product %s') % (product,)
        messages.success(request, msg)
        return redirect('dashboard:product-details', pk=product.pk)
    ctx = {
        'product_form': product_form,
        'product': product
    }
    return TemplateResponse(request, 'dashboard/product/form.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def product_select_type(request):
    form = ProductTypeSelectorForm(request.POST or None)
    status = 200
    if form.is_valid():
        redirect_url = reverse(
            'dashboard:product-add',
            kwargs={'type_pk': form.cleaned_data.get('product_type').pk})
        return (
            JsonResponse({'redirectUrl': redirect_url})
            if request.is_ajax() else redirect(redirect_url))
    elif form.errors:
        status = 400
    ctx = {'form': form}
    template = 'dashboard/product/modal/select_type.html'
    return TemplateResponse(request, template, ctx, status=status)



@staff_member_required
@permission_required('product.manage_products')
def product_toggle_is_published(request, pk):
    products = Product.objects.prefetch_related('images')
    products = products.order_by('name')
    product_types = ProductType.objects.all()
    ctx = {
        'bulk_action_form': ProductBulkUpdate(),
        'products': products,
        'product_types': product_types,
        }
    return TemplateResponse(request, 'dashboard/product/list.html', ctx)




@staff_member_required
@permission_required('product.manage_products')
def product_details(request, pk):
    products = Product.objects.prefetch_related('images').all()
    product = get_object_or_404(products, pk=pk)
    images = product.images.all()

    ctx = {
        'product': product,
        'images': images,
        }
    return TemplateResponse(request, 'dashboard/product/detail.html', ctx)



@staff_member_required
@permission_required('product.manage_products')
def product_images(request, product_pk):
    products = Product.objects.prefetch_related('images')
    product = get_object_or_404(products, pk=product_pk)
    images = product.images.all()
    ctx = {
        'product': product, 'images': images, 'is_empty': not images.exists()}
    return TemplateResponse(
        request, 'dashboard/product/product_image/list.html', ctx)


@staff_member_required
@permission_required('product.manage_products')
def product_image_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    product_image = ProductImage(product=product)
    form = ProductImageForm(
        request.POST or None, request.FILES or None, instance=product_image)
    if form.is_valid():
        product_image = form.save()
        msg = pgettext_lazy(
            'Dashboard message',
            'Added image %s') % (product_image.image.name,)
        messages.success(request, msg)
        return redirect('dashboard:product-image-list', product_pk=product.pk)
    ctx = {'form': form, 'product': product, 'product_image': product_image}
    return TemplateResponse(
        request,
        'dashboard/product/product_image/form.html',
        ctx)
