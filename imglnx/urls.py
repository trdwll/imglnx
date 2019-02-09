"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.generic import TemplateView

from . import views

from django.conf import settings
from django.conf.urls.static import static

import accounts

handler400 = 'imglnx.views.handler400'
handler403 = 'imglnx.views.handler403'
handler404 = 'imglnx.views.handler404'
handler500 = 'imglnx.views.handler500'

urlpatterns = [

	url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
	url(r'^kewlbeans/', admin.site.urls, name='admin'),
	url(r'^blog/', include('blog.urls')),
	url(r'^account/', include('accounts.urls')),

	#url(r'^(?P<filename>[a-zA-Z0-9]+)$', views.ShareView.as_view(), name='share-image'),

	url(r'^api/', include('api.urls'), name='api'),
	url(r'^latest/?$', views.LatestImagesView.as_view(), name='latest-images'),

	# album stuff
	# url(r'^album/new/?$', views.NewAlbumView.as_view(), name='newalbum'),
	url(r'^album/(?P<album_id>[a-zA-Z0-9]+)/?$', accounts.views.ViewAlbumView.as_view(), name='view_album'),

	# auth urls here, because they're just redirects
	url(r'^auth/login/?$', accounts.views.LoginUser.as_view(), name='login'),
	url(r'^auth/register/?$', accounts.views.RegisterUser.as_view(), name='register'),
	#url(r'^auth/forgot/?$', accounts.views.forgot_user.as_view(), name='forgot'),
	#url(r'^auth/forgot/reset/?$', accounts.views.forgot_user_reset.as_view(), name='forgot-reset'),
	url(r'^auth/logout/?$', logout, {'next_page': '/'}, name='logout'),

	# pages
	url(r'^page/faq/?$', TemplateView.as_view(template_name='faq.html'), name='faq'),
	url(r'^page/about/?$', TemplateView.as_view(template_name='about.html'), name='about'),
	url(r'^page/donate/?$', TemplateView.as_view(template_name='donate.html'), name='donate'),
	url(r'^page/contact/?$', views.ContactView.as_view(), name='contact'),
	url(r'^page/contact/thank-you/?$', TemplateView.as_view(template_name='misc/contact-thank-you.html'), name='contact-thanks'),
	url(r'^page/changelog/?$', TemplateView.as_view(template_name='changelog.html'), name='changelog'),
	url(r'^deleted-account/?$', TemplateView.as_view(template_name='misc/deleted-account.html'), name='deleted-account-thanks'),

	# actions
	url(r'^upload/?$', views.uploader, name='image-upload'),
	url(r'^upload/url/?$', views.url_uploader, name='url-image-upload'),

	url(r'^captcha/', include('captcha.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.ARCHIVES_URL, document_root=settings.ARCHIVES_ROOT)
	urlpatterns += static(settings.THUMBNAIL_URL, document_root=settings.THUMBNAIL_ROOT)
