from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy
from django.urls import reverse_lazy
from core.models import SiteSettings
from menu.models import Menu, MenuItem, Category
from page.models import Page
from dashboard.menu.utils import update_menu_item_linked_object
from dashboard.forms import AjaxSelect2CombinedChoiceField

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

    linked_object = AjaxSelect2CombinedChoiceField(
        querysets=[
            Category.objects.all(),
            Page.objects.all()],
        fetch_data_url=reverse_lazy('dashboard:ajax-menu-links'), min_input=0,
        required=False,
        label=pgettext_lazy('Menu item object to link', 'Link'))

    class Meta:
        model = MenuItem
        fields = ('name', 'url')
        labels = {
            'name': pgettext_lazy('Menu item name', 'Name'),
            'url': pgettext_lazy('Menu item url', 'URL')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = self.instance.linked_object
        if obj:
            obj_id = str(obj.pk) + '_' + obj.__class__.__name__
            self.   fields['linked_object'].set_initial(obj, obj_id=obj_id)

    def clean(self):
        parent = self.instance.parent
        if parent and parent.level >= 2:
            raise forms.ValidationError(
                pgettext_lazy(
                    'Menu item form error',
                    'Maximum nesting level for menu items equals to 2.'),
                code='invalid')
        url = self.cleaned_data.get('url')
        linked_object = self.cleaned_data.get('linked_object')
        if url and linked_object:
            raise forms.ValidationError(
                pgettext_lazy(
                    'Menu item form error',
                    'A single menu item can\'t point to both an internal link '
                    'and URL.'),
                code='invalid')
        if not url and not linked_object:
            raise forms.ValidationError(
                pgettext_lazy(
                    'Menu item form error',
                    'A single menu item must point to an internal link or '
                    'URL.'),
                code='invalid')
        return self.cleaned_data

    def save(self):
        linked_object = self.cleaned_data.get('linked_object')
        return update_menu_item_linked_object(self.instance, linked_object)