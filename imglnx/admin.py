"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from . models import Contact, Alert, UploadedImage, Album
#from accounts.models import UserProfile

# class UserInline(admin.StackedInline):
# 	model = UserProfile
# 	can_delete = False
# 	verbose_name = 'User Profile Data'
# 	verbose_name_plural = 'User Profile Data'

class UserSearch(admin.ModelAdmin):
	search_fields = ['username']
	#inlines = (UserInline, )

class ImageSearch(admin.ModelAdmin):
	search_fields = ['username', 'image', 'api_upload_key', 'upload_date']

class AlbumSearch(admin.ModelAdmin):
	search_fields = ['username', 'title', 'album_id']


admin.site.unregister(User)
admin.site.register(User, UserSearch)
admin.site.register(Contact)
admin.site.register(Alert)
admin.site.register(UploadedImage, ImageSearch)
admin.site.register(Album, AlbumSearch)