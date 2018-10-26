"""AztpaFactory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='staff-index'),
    url(r'^staff-create/$', views.staff_create, name='staff-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.staff_details, name='staff-details'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.staff_delete, name='staff-delete'),
    #url(r'^(?P<slug>[\w-]+)/$', views.settings_details, name='settings-details'),
   # url(r'^(?P<slug>[\w-]+)/edit/$', views.settings_edit, name='settings-edit'),
]