"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.contrib import admin
from . models import Post

class BlogAdmin(admin.ModelAdmin):
	exclude = ['posted']
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, BlogAdmin)