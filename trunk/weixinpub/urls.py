#!/usr/bin/env python
# coding=utf-8
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url

from weixinpub import views



urlpatterns = patterns('',
    url(r'^$', views.weixinpub, name='weixinpub'),
    url(r'^about$', views.about, name='about'),
)

#urlpatterns += staticfiles_urlpatterns()

