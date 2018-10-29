from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.sites.models import Site
from django.utils.translation import pgettext_lazy, ugettext_lazy
from django.contrib.auth import password_validation

from account.models import User


class StaffCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone', 'is_superuser', 'first_name', 'last_name', 'user_permissions', 'groups', 'is_active', 'last_login', 'note']
        exclude = ['password']


class StaffChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email','password', 'phone', 'is_superuser', 'first_name', 'last_name', 'user_permissions', 'groups', 'is_active', 'last_login', 'note']

    def save(self, commit=False):
        user = super().save()
        user.set_password(self.cleaned_data['password'])
        print(self.cleaned_data['password'])
        if commit:
            user.save()
        return user