#!/usr/bin/env python
# -*- coding:utf-8 -*-  

from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
# from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
#admin.autodiscover()

from summer_2015 import settings

#url配置
urlpatterns = patterns('',
    url(r'', include("summerManagement.urls")),
)+static(settings.STATIC_URL)


#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

