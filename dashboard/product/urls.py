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
    url(r'^types/$', views.product_type_list, name='product-type-list'),
    url(r'^types/add/$', views.product_type_create, name='product-type-add'),
    url(r'^types/(?P<pk>[0-9]+)/update/$', views.product_type_edit, name='product-type-update'),
    url(r'^types/(?P<pk>[0-9]+)/delete/$', views.product_type_delete, name='product-type-delete'),

    url(r'attributes/$', views.attribute_list, name='attributes'),
    url(r'attributes/(?P<pk>[0-9]+)/$', views.attribute_details, name='attribute-details'),
    url(r'attributes/add/$', views.attribute_create, name='attribute-add'),
    url(r'attributes/(?P<pk>[0-9]+)/update/$', views.attribute_edit, name='attribute-update'),
    url(r'attributes/(?P<pk>[0-9]+)/delete/$', views.attribute_delete, name='attribute-delete'),
    url(r'attributes/(?P<attribute_pk>[0-9]+)/value/add/$', views.attribute_value_create, name='attribute-value-add'),
    url(r'attributes/(?P<attribute_pk>[0-9]+)/value/(?P<value_pk>[0-9]+)/update/$', views.attribute_value_edit,name='attribute-value-update'),
    url(r'attributes/(?P<attribute_pk>[0-9]+)/value/(?P<value_pk>[0-9]+)/delete/$',views.attribute_value_delete,name='attribute-value-delete'),
    url(r'attributes/(?P<attribute_pk>[0-9]+)/values/reorder/$', views.ajax_reorder_attribute_values,name='attribute-values-reorder')
]
