"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
	title = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(max_length=128, unique=True)
	body = models.TextField()
	publish = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		kwargs = {
			'slug': self.slug,
			'year': '%04d' % self.created.year,
			'month': '%02d' % self.created.month
		}

		return reverse('blog:view_post', kwargs=kwargs)

	class Meta:
		app_label = 'imglnx'
		verbose_name = 'Blog Post'
		verbose_name_plural = 'Blog Posts'
