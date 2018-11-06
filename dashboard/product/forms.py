import json

from django import forms
from product.models import Attribute, ProductType, AttributeValue, Product, Category, ProductImage
from django.utils.translation import pgettext_lazy
from django.db.models import Q
from . import ProductBulkAction
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.forms import TreeNodeChoiceField
from ..seo.fields import SeoDescriptionField, SeoTitleField
from ..seo.utils import prepare_seo_description
from ..forms import ModelChoiceOrCreationField, OrderedModelMultipleChoiceField
from django.utils.text import slugify
from django.utils.encoding import smart_text
from product.thumbnails import create_product_thumbnails
from .widgets import ImagePreviewWidget


class ProductTypeForm(forms.ModelForm):
    product_attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.none(), required=False,
        label=pgettext_lazy(
            'Product type attributes', 'Attributes common to all variants.'))

    class Meta:
        model = ProductType
        exclude = []
        labels = {
            'name': pgettext_lazy(
                'Item name',
                'Name'), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unassigned_attrs_q = Q(
            product_type__isnull=True)

        if self.instance.pk:
            product_attrs_qs = Attribute.objects.filter(
                Q(product_type=self.instance) | unassigned_attrs_q)
            product_attrs_initial = self.instance.product_attributes.all()
        else:
            unassigned_attrs = Attribute.objects.filter(unassigned_attrs_q)
            product_attrs_qs = unassigned_attrs
            product_attrs_initial = []

        self.fields['product_attributes'].queryset = product_attrs_qs
        self.fields['product_attributes'].initial = product_attrs_initial

    def clean(self):
        data = super().clean()
        product_attr = set(self.cleaned_data.get('product_attributes', []))

        if product_attr:
            msg = pgettext_lazy(
                'Product type form error',
                'A single attribute can\'t belong to both a product '
                'and its variant.')

        if not self.instance.pk:
            return data
        return data

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        new_product_attrs = self.cleaned_data.get('product_attributes', [])
        instance.product_attributes.set(new_product_attrs)
        return instance


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = []
        labels = {
            'name': pgettext_lazy(
                'Product display name', 'Display name'),
            'slug': pgettext_lazy(
                'Product internal name', 'Internal name')}

class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'name']
        widgets = {'attribute': forms.widgets.HiddenInput()}
        labels = {
            'name': pgettext_lazy(
                'Item name', 'Name')}



class ProductBulkUpdate(forms.Form):
    """Perform one selected bulk action on all selected products."""

    action = forms.ChoiceField(choices=ProductBulkAction.CHOICES)
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    def save(self):
        action = self.cleaned_data['action']
        if action == ProductBulkAction.PUBLISH:
            self._publish_products()
        elif action == ProductBulkAction.UNPUBLISH:
            self._unpublish_products()

    def _publish_products(self):
        self.cleaned_data['products'].update(is_published=True)

    def _unpublish_products(self):
        self.cleaned_data['products'].update(is_published=False)


class ProductTypeSelectorForm(forms.Form):

    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.all(),
        label=pgettext_lazy('Product type form label', 'Product type'),
        widget=forms.RadioSelect, empty_label=None)





class AttributesMixin:
    """Form mixin that dynamically adds attribute fields."""

    available_attributes = Attribute.objects.none()

    # Name of a field in self.instance that hold attributes HStore
    model_attributes_field = None

    def __init__(self, *args, **kwargs):
        if not self.model_attributes_field:
            raise Exception(
                'model_attributes_field must be set in subclasses of '
                'AttributesMixin.')

    def prepare_fields_for_attributes(self):
        initial_attrs = getattr(self.instance, self.model_attributes_field)
        for attribute in self.available_attributes:
            field_defaults = {
                'label': attribute.name,
                'required': False,
                'initial': initial_attrs.get(str(attribute.pk))}
            if attribute.has_values():
                field = ModelChoiceOrCreationField(
                    queryset=attribute.values.all(), **field_defaults)
            else:
                field = forms.CharField(**field_defaults)
            self.fields[attribute.get_formfield_name()] = field

    def iter_attribute_fields(self):
        for attr in self.available_attributes:
            yield self[attr.get_formfield_name()]

    def get_saved_attributes(self):
        attributes = {}
        for attr in self.available_attributes:
            value = self.cleaned_data.pop(attr.get_formfield_name())
            if value:
                # if the passed attribute value is a string,
                # create the attribute value.
                if not isinstance(value, AttributeValue):
                    value = AttributeValue(
                        attribute_id=attr.pk, name=value, slug=slugify(value))
                    value.save()
                attributes[smart_text(attr.pk)] = smart_text(value.pk)
        return attributes





class ProductForm(forms.ModelForm, AttributesMixin):

    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        label=pgettext_lazy('Category', 'Category'))
    description = RichTextUploadingField(
       )

    model_attributes_field = 'attributes'

    class Meta:
        model = Product
        exclude = ['attributes', 'product_type', 'updated_at']
        labels = {
            'name': pgettext_lazy('Item name', 'Name'),
            'available_on': pgettext_lazy(
                'Availability date', 'Publish product on'),
            'is_published': pgettext_lazy(
                'Product published toggle', 'Published'),
      }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_type = self.instance.product_type
        self.available_attributes = (
            product_type.product_attributes.prefetch_related('values').all())
        self.prepare_fields_for_attributes()
        self.fields['seo_description'] = SeoDescriptionField(
            extra_attrs={
                'data-bind': self['description'].auto_id,
                'data-materialize': self['description'].html_name})
        self.fields['seo_title'] = SeoTitleField(
            extra_attrs={'data-bind': self['name'].auto_id})

    def clean_seo_description(self):
        seo_description = prepare_seo_description(
            seo_description=self.cleaned_data['seo_description'],
            html_description=self.data['description'],
            max_length=self.fields['seo_description'].max_length)
        return seo_description

    def save(self, commit=True):
        attributes = self.get_saved_attributes()
        self.instance.attributes = attributes
        instance = super().save()
        return instance




class ProductImageForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ProductImage
        exclude = ('product', 'sort_order')
        labels = {
            'image': pgettext_lazy('Product image', 'Image'),
            'alt': pgettext_lazy(
                'Description', 'Description')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.image:
            self.fields['image'].widget = ImagePreviewWidget()

    def save(self, commit=True):
        image = super().save(commit=commit)
        create_product_thumbnails.delay(image.pk)
        return image