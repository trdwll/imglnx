"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.conf.urls import url
from . import views


app_name = 'account'
urlpatterns = [
	#url(r'^$', views.user_dashboard, name='dashboard'),
	url(r'^$', views.UpdateProfileView.as_view(), name='dashboard'),
	url(r'^delete/?$', views.DeleteAccountView.as_view(), name='delete-account'),
	url(r'^download/?$', views.DownloadView.as_view(), name='download-account'),
#	url(r'^code/?$', views.SetRecoveryCode.as_view(), name='set-recovery-code'),
	url(r'^images/?$', views.ImagesView.as_view(), name='images'),
	url(r'^images/change/?$', views.ChangeImageVisibility.as_view(), name='change-visibility-images'),

	# album shit
	url(r'^images/add/?$', views.AddToAlbum.as_view(), name='add-to-album'),
	url(r'^albums/delete/?$', views.DeleteAlbum.as_view(), name='delete-album'),
	url(r'^albums/remove/?$', views.RemoveImageAlbum.as_view(), name='remove-image-album'),
	url(r'^albums/?$', views.AlbumsView.as_view(), name='albums'),
]
