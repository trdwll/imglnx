"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'api'
urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='api.html'), name='api-home'),
	url(r'^generate/?$', views.CreateKey.as_view(), name='api-create-key'),
	url(r'^delete/?$', views.DeleteKey.as_view(), name='api-delete-key'),
	url(r'^v1.1/upload/?$', views.ApiUpload.as_view(), name='api-upload'),
]
