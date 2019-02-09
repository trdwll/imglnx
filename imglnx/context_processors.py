"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.conf import settings

from . models import Alert

def global_settings(request):
	alerts = Alert.objects.all()
	return {
		'VERSION': settings.APP_VERSION,
		'alerts': alerts,
		'MEDIA_URL': settings.MEDIA_URL,
		'ARCHIVES_URL': settings.ARCHIVES_URL
	}