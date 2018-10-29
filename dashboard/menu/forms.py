from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy

from core.models import SiteSettings
from menu.models import Menu, MenuItem


class AssignMenuForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ('top_menu', 'bottom_menu')


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name',)
        labels = {
            'name': pgettext_lazy('Menu name', 'Menu name')}


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name',)
        labels = {
            'name': pgettext_lazy('Menu name', 'Menu name')}