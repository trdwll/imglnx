"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django import template
from django.conf import settings
import os

from django.contrib.auth.models import User
from imglnx.models import UploadedImage, Album

register = template.Library()

from imglnx.utilities import get_size, human_readable

@register.filter(name='get_hosted_count')
def get_hosted_count(dir):
	return len([f for f in os.listdir(settings.MEDIA_ROOT) if not f.endswith('.zip')])

@register.filter(name='get_hosted_size')
def get_hosted_size(dir):
	return human_readable(get_size(settings.MEDIA_ROOT))

@register.filter(name='get_user_images_count')
def get_user_images_count(username):
	return UploadedImage.objects.all().filter(username=username).count()

@register.filter(name='get_user_albums_count')
def get_user_albums_count(username):
	return Album.objects.all().filter(username=username).count()

@register.filter(name='get_album_size')
def get_album_size(id):
	return UploadedImage.objects.filter(album_id=id).count()

# cover image for the album
@register.filter(name='get_album_image')
def get_album_image(id):
	img = UploadedImage.objects.filter(album_id=id).values_list('image', flat=True).first() 

	if img:
		if os.path.isfile(settings.THUMBNAIL_ROOT+'/'+str(img)):
			return settings.THUMBNAIL_URL+str(img)
			
		return settings.MEDIA_URL+img

	return '/static/img/no_images_in_album.png'

@register.filter(name='get_thumbnail')
def get_thumbnail(image):
	if os.path.isfile(settings.THUMBNAIL_ROOT+'/'+str(image)):
		return settings.THUMBNAIL_URL+str(image)

	return settings.MEDIA_URL+str(image)