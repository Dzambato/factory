from django.contrib import admin
from .models import ProductType, Attribute
# Register your models here.

admin.site.register(ProductType)
admin.site.register(Attribute)