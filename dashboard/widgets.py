from django_filters.widgets import RangeWidget
from django_prices.widgets import MoneyInput
from django.forms import Textarea, TextInput
from django import forms
from django.conf import settings

class DateRangeWidget(RangeWidget):
    def __init__(self, attrs=None):
        widgets = (forms.DateInput, forms.DateInput)
        # pylint: disable=bad-super-call
        super(RangeWidget, self).__init__(widgets, attrs)


class CharsLeftWidget(TextInput):
    """Displays number of characters left on the right side of the label,
    requires different rendering on the frontend.
    """
    pass


class MoneyRangeWidget(RangeWidget):
    def __init__(self, attrs=None):
        self.currency = getattr(settings, 'DEFAULT_CURRENCY')
        widgets = (MoneyInput(self.currency), MoneyInput(self.currency))
        # pylint: disable=bad-super-call
        super(RangeWidget, self).__init__(widgets, attrs)