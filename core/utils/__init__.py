from django.core.paginator import InvalidPage, Paginator
from django.conf import settings
import logging
from django.contrib.sites.models import Site
from django.http import Http404
from urllib.parse import urljoin
from django.utils.encoding import iri_to_uri, smart_text
from versatileimagefield.image_warmer import VersatileImageFieldWarmer


logger = logging.getLogger(__name__)

def get_paginator_items(items,page_number):
        paginator = Paginator(items, settings.DASHBOARD_PAGINATE_BY)
        if not page_number:
            page_number = 1
        try:
            page_number = int(page_number)
        except ValueError:
            raise Http404('Page can not be converted to an int.')

        try:
            items = paginator.page(page_number)
        except InvalidPage as err:
            raise Http404('Invalid page (%(page_number)s): %(message)s' % {
                'page_number': page_number, 'message': str(err)})
        return items


def build_absolute_uri(location):
    # type: (str) -> str
    host = Site.objects.get_current().domain
    protocol = 'https' if settings.ENABLE_SSL else 'http'
    current_uri = '%s://%s' % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)



def create_thumbnails(pk, model, size_set, image_attr=None):
    instance = model.objects.get(pk=pk)
    if not image_attr:
        image_attr = 'image'
    image_instance = getattr(instance, image_attr)
    if image_instance.name == '':
        # There is no file, skip processing
        return
    warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set=size_set, image_attr=image_attr)
    logger.info('Creating thumbnails for  %s', pk)
    num_created, failed_to_create = warmer.warm()
    if num_created:
        logger.info('Created %d thumbnails', num_created)
    if failed_to_create:
        logger.error('Failed to generate thumbnails',
                     extra={'paths': failed_to_create})
