#!/usr/bin/env python
# coding=utf-8
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'soulife.views.home', name='home'),
    # url(r'^soulife/', include('soulife.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('main_page.urls')),
    url(r'^weixinpub', include('weixinpub.urls')),
    url(r'^weixinpub/', include('weixinpub.urls')),
)

#urlpatterns += staticfiles_urlpatterns()
