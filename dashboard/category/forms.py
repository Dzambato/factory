from django import forms
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy

from product.models import Category
from ..seo.fields import SeoDescriptionField, SeoTitleField


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ['slug']

        labels = {
            'name': pgettext_lazy('Item name', 'Name'),
            'description': pgettext_lazy('Description', 'Description'),
            'background_image': pgettext_lazy(
                'Category form',
                'Background Image')}


    def __init__(self, *args, **kwargs):
        self.parent_pk = kwargs.pop('parent_pk')
        super().__init__(*args, **kwargs)
        self.fields['seo_description'] = SeoDescriptionField(
            extra_attrs={'data-bind': self['description'].auto_id})
        self.fields['seo_title'] = SeoTitleField(
            extra_attrs={'data-bind': self['name'].auto_id})

    def save(self, commit=True):
        if self.parent_pk:
            self.instance.parent = get_object_or_404(
                Category, pk=self.parent_pk)
        return super().save(commit=commit)