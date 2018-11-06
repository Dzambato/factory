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
    url(r'^$', views.page_list, name='page-list'),
    url(r'^add/$', views.page_add, name='page-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.page_details, name='page-details'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.page_update, name='page-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.page_delete, name='page-delete')
]
