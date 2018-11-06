from django.db import models
from pytils.translit import slugify
from core.models import SortableModel
from django.utils.translation import pgettext_lazy
import datetime
from seo.models import SeoModel
from autoslug import AutoSlugField
from django.urls import reverse
from menu.models import Category
from versatileimagefield.fields import PPOIField, VersatileImageField
from django.contrib.postgres.fields import HStoreField
# Create your models here.


class ProductType(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        app_label = 'product'

    def __str__(self):
        return self.name

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)

class Product(SeoModel):
    slug = AutoSlugField(populate_from='name',unique=True)
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    available_on = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    attributes = HStoreField(default=dict, blank=True)


    class Meta:
        app_label = 'product'
        permissions = ((
            'manage_products', pgettext_lazy(
                'Permission description',
                'Manage products.')),)


    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'product:details',
            kwargs={'slug': self.slug, 'product_id': self.id})

    def is_available(self):
        today = datetime.date.today()
        return self.available_on is None or self.available_on <= today

    def get_first_image(self):
        images = list(self.images.all())
        return images[0].image if images else None



class Attribute(models.Model):
    slug = AutoSlugField(populate_from='name',unique=True)
    name = models.CharField(max_length=50)
    product_type = models.ForeignKey(ProductType, related_name='product_attributes', blank=True,null=True, on_delete=models.CASCADE)


    class Meta:
        ordering = ('slug', )

    def __str__(self):
        return self.name

    def get_formfield_name(self):
        return slugify('attribute-%s' % self.slug)

    def has_values(self):
        return self.values.exists()




class AttributeValue(SortableModel):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)

    class Meta:
        ordering = ('sort_order',)
        unique_together = ('name', 'attribute')

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.attribute.values.all()


class ProductImage(SortableModel):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = VersatileImageField(
        upload_to='products', ppoi_field='ppoi', blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('sort_order', )
        app_label = 'product'

    def get_ordering_queryset(self):
        return self.product.images.all()
