import json

from django import forms
from django.core.exceptions import ValidationError
from product.models import Attribute, ProductType, AttributeValue
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import pgettext_lazy
from django.db.models import Q


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
