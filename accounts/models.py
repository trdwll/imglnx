"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.db.models.signals import post_save
from django.dispatch import receiver

#class UserProfile(models.Model):
	#user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofiles", related_query_name="userprofile")
	#email = models.CharField(max_length=128)
	#recovery_key = models.CharField(max_length=64)


# causes imglnx to break - on user login it returns a 500 error
#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
#	if created:
#		UserProfile.objects.create(user=instance)
#	instance.userprofile.save()