from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import pgettext_lazy
from django.db.models import F, Max
from . import AuthenticationBackends


class SiteSettings(models.Model):
    slug = models.SlugField(unique=True)
    site = models.OneToOneField(Site, related_name='settings', on_delete=models.CASCADE)
    header_text = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500, blank=True)
    top_menu = models.ForeignKey('menu.Menu', on_delete=models.SET_NULL, verbose_name=pgettext_lazy('Top menu', 'Top menu field'), related_name='+', blank=True,null=True)
    bottom_menu = models.ForeignKey('menu.Menu', on_delete=models.SET_NULL, verbose_name=pgettext_lazy('Bottom menu', 'Bottom menu field'), related_name='+', blank=True,null=True)
    #include_taxes_in_prices = models.BooleanField(default=True)
    #display_gross_prices = models.BooleanField(default=True)
    #charge_taxes_on_shipping = models.BooleanField(default=True)
    #track_inventory_by_default = models.BooleanField(default=True)
    #homepage_collection = models.ForeignKey('product.Collection', on_delete=models.SET_NULL, related_name='+',blank=True, null=True)
    #default_weight_unit = models.CharField(max_length=10, choices=WeightUnits.CHOICES,default=WeightUnits.KILOGRAM)

    class Meta:
        permissions = ((
            'manage_settings', pgettext_lazy(
                'Permission description', 'Manage settings.')),)

    def __str__(self):
        return self.site.name

    def available_backends(self):
        return self.authorizationkey_set.values_list('name', flat=True)


class AuthorizationKey(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, choices=AuthenticationBackends.BACKENDS)
    key = models.TextField()
    password = models.TextField()

    class Meta:
        unique_together = (('site_settings', 'name'),)

    def __str__(self):
        return self.name

    def key_and_secret(self):
        return self.key, self.password



class SortableModel(models.Model):
    sort_order = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError('Unknown ordering queryset')

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('sort_order'))
            existing_max = existing_max.get('sort_order__max')
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        qs = self.get_ordering_queryset()
        qs.filter(sort_order__gt=self.sort_order).update(
            sort_order=F('sort_order') - 1)
        super().delete(*args, **kwargs)