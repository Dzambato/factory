from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from core.utils import build_absolute_uri
from django.utils.translation import pgettext_lazy
import datetime
from seo.models import SeoModel
from autoslug import AutoSlugField

class Page(SeoModel):
    slug = AutoSlugField(populate_from='title', unique=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField ()
    created = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)
    available_on = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('slug',)
        permissions = ((
            'manage_pages', pgettext_lazy(
                'Permission description', 'Manage pages.')),)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page:details', kwargs={'slug': self.slug})

    def get_full_url(self):
        return build_absolute_uri(self.get_absolute_url())

    @property
    def is_published(self):
        today = datetime.date.today()
        return self.is_visible and (
            self.available_on is None or self.available_on <= today)
