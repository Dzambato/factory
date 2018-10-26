from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from ..views import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from core.models import SiteSettings

from .forms import SiteForm, SiteSettingsForm

# Create your views here.

@staff_member_required
@permission_required('core.manage_settings')
def index(request):
    site = get_current_site(request)
    site_settings = site.settings
    print('sssssssssssssss')
    return redirect('dashboard:settings-details', slug=site_settings.slug)


@staff_member_required
@permission_required('core.manage_settings')
def settings_details(request, slug):
    site_settings = get_object_or_404(SiteSettings,slug=slug)
    # Дополнить ключи авторизации
    ctx = {
        'site_settings' : site_settings,
    }
    return render(request, 'dashboard/settings/detail.html', ctx)


@staff_member_required
@permission_required('core.manage_settings')
def settings_edit(request, slug):
    site_settings = get_object_or_404(SiteSettings,slug=slug)
    site_form = SiteForm(request.POST or None, instance=site_settings.site)
    site_settings_form = SiteSettingsForm(request.POST or None, instance=site_settings)
    if request.POST:
        if (site_form.has_changed() and site_form.is_valid()) or (site_settings_form.has_changed() and site_settings_form.is_valid()):
            site_form.save()
            site_settings_form.save()
            return redirect('dashboard:settings-details', slug=site_settings.slug)
    ctx = {
        'site_settings' : site_settings,
        'site_form' : site_form,
        'site_settings_form' : site_settings_form
    }
    return TemplateResponse(request, 'dashboard/settings/form.html', ctx)
