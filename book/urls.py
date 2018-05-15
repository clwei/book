"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', auth_views.logout),
    url(r'^book/$', views.book),
    url(r'^book/add$', views.book_add),
    url(r'^book/(?P<book_id>\d+)/$', views.book_view),
    url(r'^book/delete/(?P<book_id>\d+)/$', views.book_delete),
    url(r'^reader/$', views.reader),
    url(r'^reader/add/$', views.reader_add),
    url(r'^reader/delete/(?P<reader_id>\d+)/$', views.reader_delete),
    url(r'^reader/(?P<reader_id>\d+)/$', views.reader_view),
    url(r'^circulation/$', views.circulation),
]
