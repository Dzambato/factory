from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import pgettext_lazy
from mptt.managers import TreeManager
from django.urls import reverse
from mptt.models import MPTTModel
from versatileimagefield.fields import PPOIField, VersatileImageField
from seo.models import SeoModel
from core.models import SortableModel

# Create your models here.


class Menu(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=128)
    json_content = JSONField(blank=True, default=dict)

    class Meta:
        permissions = ((
                           'manage_menus', pgettext_lazy(
                               'Permission description', 'Manage navigation.')),)

    def __str__(self):
        return self.name


class Category(MPTTModel, SeoModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)
    background_image = VersatileImageField(
        upload_to='category-backgrounds', blank=True, null=True)

    objects = models.Manager()
    tree = TreeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'product:category',
            kwargs={'slug': self.slug, 'category_id': self.id})


class MenuItem(MPTTModel, SortableModel):
    menu = models.ForeignKey(
        Menu, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)

    url = models.URLField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    # collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.CASCADE)
    page = models.ForeignKey('page.Page', blank=True, null=True, on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        ordering = ('sort_order',)
        app_label = 'menu'

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return (
            self.menu.items.all() if not self.parent
            else self.parent.children.all())

    @property
    def linked_object(self):
        return self.category or self.page

    def get_url(self):
        linked_object = self.linked_object
        return linked_object.get_absolute_url() if linked_object else self.url

    @property
    def destination_display(self):
        linked_object = self.linked_object

        if not linked_object:
            prefix = pgettext_lazy('Link object type description', 'URL: ')
            return prefix + self.url

        if isinstance(linked_object, Category):
            prefix = pgettext_lazy(
                'Link object type description', 'Category: ')
        else:
            prefix = pgettext_lazy(
                'Link object type description', 'Page: ')

        return prefix + str(linked_object)

    def is_public(self):
        return not self.linked_object or getattr(
            self.linked_object, 'is_published', True)