from django import forms
from . import ProductBulkAction

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
