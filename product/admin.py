from django.contrib import admin
from .models import ProductType, Attribute, Product
# Register your models here.

admin.site.register(ProductType)
admin.site.register(Attribute)
admin.site.register(Product)