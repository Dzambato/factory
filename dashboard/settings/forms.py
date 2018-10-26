from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy

from core.models import SiteSettings


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = []
        labels = {
            'domain': pgettext_lazy(
                'Domain name (FQDN)', 'Domain name'),
            'name': pgettext_lazy(
                'Display name', 'Display name')}


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'header_text', 'description', 'top_menu', 'bottom_menu']
        labels = {
            'header_text': pgettext_lazy(
                'Header text', 'Header text'),
            'description': pgettext_lazy(
                'Description', 'Description'),
            'top_menu': pgettext_lazy('Top menu text', 'Top menu text'),
            'bottom_menu': pgettext_lazy('Bottom menu text', 'Bottom menu text'), }
