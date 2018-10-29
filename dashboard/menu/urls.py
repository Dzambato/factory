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
    url(r'^$', views.index, name='menu-index'),
    url(r'^add/$', views.menu_create, name='menu-add'),
    url(r'^(?P<pk>[0-9]+)/delete/$',views.menu_delete, name='menu-delete'),
    url(r'^(?P<pk>[\w-]+)/$', views.menu_details, name='menu-details'),
    url(r'^(?P<pk>[\w-]+)/edit/$', views.menu_edit, name='menu-edit'),
    url(r'^(?P<menu_pk>[0-9]+)/item/(?P<item_pk>[0-9]+)/$',views.menu_item_details, name='menu-item-details'),
   # url(r'^(?P<slug>[\w-]+)/edit/$', views.settings_edit, name='settings-edit'),
]
