from django.contrib import admin
from .models import Category, MenuItem, Menu

# Register your models here.

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(MenuItem)