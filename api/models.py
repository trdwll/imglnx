"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.db import models

# Create your models here.
class APIKeys(models.Model):
	username = models.CharField(max_length=256)
	description = models.CharField(max_length=512)
	api_key = models.CharField(max_length=128)
	upload_count = models.IntegerField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username + ' - ' + str(self.created)

	class Meta:
		app_label = 'imglnx'
		verbose_name = 'API Key'
		verbose_name_plural = 'API Keys'