from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy

from core.models import SiteSettings


class AssignMenuForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ('top_menu', 'bottom_menu')