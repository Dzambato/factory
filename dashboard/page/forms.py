import json

from django import forms
from django.core.exceptions import ValidationError
from page.models import Page
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import pgettext_lazy


class PageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Page
        exclude = ['created','slug']
        labels = {
            'title': pgettext_lazy(
                'Page form: title field', 'Title'),
            'content': pgettext_lazy('Content text', 'Content'),
            'available_on': pgettext_lazy(
                'Page form: available on which date field', 'Available on'),
            'is_visible': pgettext_lazy(
                'Page form: visibility status indicator', 'Is visible')}
        help_texts = {
            'is_visible': pgettext_lazy(
                'Form field visibility status',
                'Form field visibility status')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_slug(self):
        # Make sure slug is not being written to database with uppercase.
        slug = self.cleaned_data.get('slug')
        slug = slug.lower()
        return slug


