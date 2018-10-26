from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy

from account.models import User


class StaffForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone', 'is_superuser', 'first_name', 'last_name', 'user_permissions', 'is_active', 'last_login', 'note']
        exclude = ['password', 'groups']