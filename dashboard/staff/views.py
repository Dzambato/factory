from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy
from ..views import staff_member_required
from core.utils import get_paginator_items


from account.models import User

from .forms import StaffForm

# Create your views here.

@staff_member_required
@permission_required('account.manage_users')
def index(request):
    staff_members = User.objects.filter(is_staff=True).order_by('username')
    #staff_filter = StaffFilter(request.GET, queryset=staff_members)
    staff_members = get_paginator_items(
        staff_members,
        request.GET.get('page'))
    ctx = {
        'staff_list': staff_members,
        #'filter_set': staff_filter,
        #'is_empty': not staff_filter.queryset.exists()
    }
    return TemplateResponse(request, 'dashboard/staff/index.html', ctx)


@staff_member_required
@permission_required('account.manage_staff')
def staff_create(request):
    form = StaffForm(request.POST or None, instance=User())
    print(form)
    if request.POST and form.is_valid() :
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Created staff member %s') % (form['username'],)
        messages.success(request, msg)
        return redirect('dashboard:staff-index')
    ctx = {'staff_form': form}
    return TemplateResponse(request, 'dashboard/staff/detail.html', ctx)



def staff_details (request, pk):
    staff_member =  get_object_or_404(User, is_staff=True, pk=pk)
    staff_form = StaffForm( request.POST or None, instance=staff_member)
    if request.POST and staff_form.is_valid() and staff_form.has_changed():
        staff_form.save()
        print(request.POST)
        msg = pgettext_lazy(
            'Dashboard message', 'Updatmed staff member %s')
        messages.success(request, msg)
        return redirect('dashboard:staff-index')
    ctx = {
        'staff_member': staff_member,
        'staff_form': staff_form,
    }
    return TemplateResponse(request, 'dashboard/staff/detail.html', ctx)


def staff_delete (request, pk):
    staff_member =  get_object_or_404(User, is_staff=True, pk=pk)
    staff_form = StaffForm( request.POST or None, instance=staff_member)
    if request.POST and staff_form.is_valid() and staff_form.has_changed():
        staff_form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated staff member %s') % (staff_member,)
        messages.success(request, msg)
        return redirect('dashboard:staff-index')
    ctx = {
        'staff_member': staff_member,
        'staff_form': staff_form,
    }
    return TemplateResponse(request, 'dashboard/staff/detail.html', ctx)
