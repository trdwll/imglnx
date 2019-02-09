"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.blog_home, name='index'),
    url(r'^post/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[^\.]+).html', views.view_post, name='view_post')
]
