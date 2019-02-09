"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django import forms
from . models import Contact, Album
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list


class ContactForm(forms.ModelForm):
	captcha = CaptchaField()

	class Meta:
		model = Contact
		fields = [
			'email',
			'reason',
			'message',
			'captcha'
		]


#class NewAlbumForm(forms.ModelForm):

	# class Meta:
	# 	model = Album
	# 	fields = ['title', 'album_image']
	# 	labels = {
	# 		"album_image": _("Album Image"),
	# 		"title": _("Album Title")
	# 	}

