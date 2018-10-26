import uuid
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.utils.translation import pgettext_lazy, ugettext_lazy
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser)

def get_token():
    return str(uuid.uuid4())

class User(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)
    token = models.UUIDField(default=get_token, editable=False, unique=True)
    note = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=True,
        help_text=ugettext_lazy('Designates whether the user can log into this admin site.'),
    )
    class Meta:
        permissions = (
            (
                'manage_users', pgettext_lazy(
                    'Permission description', 'Manage customers.')),
            (
                'manage_staff', pgettext_lazy(
                    'Permission description', 'Manage staff.')),
            )