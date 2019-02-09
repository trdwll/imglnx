"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.urlresolvers import reverse
# from django.core.validators import validate_comma_separated_integer_list
from django.conf import settings
import os

class Contact(models.Model):
	email = models.CharField(max_length=128)
	reason = models.CharField(max_length=128) 
	message = models.CharField(max_length=4096)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.reason + ' - ' + str(self.created)

	class Meta:
		verbose_name = 'Contact Request'
		verbose_name_plural = 'Contact Requests'


class Alert(models.Model):
	STYLES = (
		('success', 'Success'),
		('info', 'Info'),
		('warning', 'Warning'),
		('danger', 'Danger')
	)

	title = models.CharField(max_length=256)
	style = models.CharField(max_length=7, choices=STYLES)
	body = models.TextField()
	sticky = models.BooleanField()

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Alert'
		verbose_name_plural = 'Alerts'


class Album(models.Model):
	username = models.CharField(max_length=128)
	album_id = models.CharField(max_length=64)
	title = models.CharField(max_length=32)
	is_private = models.BooleanField(default=False)

	def __str__(self):
		return self.username + ' - ' + self.title

	def get_url(self):
		kwargs = {
			'album_id': self.album_id
		}

		return reverse('view_album', kwargs=kwargs)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Album'
		verbose_name_plural = 'Albums'


class UploadedImage(models.Model):
	album_id = models.CharField(max_length=9)
	username = models.CharField(max_length=128)
	image = models.FileField(default='static/img/image_not_found.png')
	upload_date = models.DateTimeField(auto_now_add=True)
	is_private = models.BooleanField(default=0)
	api_upload_key = models.CharField(max_length=128, default='NULL', blank=True)
	api_upload = models.BooleanField(default=0)

	def __str__(self):
		return self.username + ' - ' + str(self.image) + ' - ' + str(self.upload_date)

	def delete(self, *args, **kwargs):
		img = self.image
		if os.path.isfile(settings.THUMBNAIL_ROOT+'/'+str(img)):
			os.remove(settings.THUMBNAIL_ROOT+'/'+str(img))

		img.delete()
		return super(UploadedImage, self).delete(*args, **kwargs)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Uploaded Image'
		verbose_name_plural = 'Uploaded Images'


@receiver(pre_delete, sender=UploadedImage)
def UploadedImage_delete(sender, instance, **kwargs):
 	instance.image.delete(False)

