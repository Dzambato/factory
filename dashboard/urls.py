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
from django.urls import path, include
from django.conf.urls import url
from .settings.urls import urlpatterns as settings_urls
from .menu.urls import urlpatterns as menu_urls
from .staff.urls import urlpatterns as staff_urls
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^settings/', include(settings_urls)),
    url(r'^menu/', include(menu_urls)),
    url(r'^staff/', include(staff_urls)),
]
