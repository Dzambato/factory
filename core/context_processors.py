from django.contrib.sites.shortcuts import get_current_site
from django.db.models import prefetch_related_objects


def site(request):
    site = get_current_site(request) # Получаем текущий сайт из SITE_ID в settings или из request.get_host() через модель Site
    prefetch_related_objects(
        [site], 'settings')
    return {'site': site}
