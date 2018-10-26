from django.shortcuts import render
from django.contrib.admin.views.decorators import (staff_member_required as _staff_member_required, user_passes_test)

# Create your views here.

def staff_member_required(f):
    return _staff_member_required(f,login_url='account:login')

@staff_member_required
def index(request):
    return render(request,'dashboard/index.html')