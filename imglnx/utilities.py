"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
import os
import hashlib
import subprocess

from .models import UploadedImage
from django.conf import settings

def get_size(start_path = '.', filter='.zip'):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			if not f.endswith(filter):
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
	return total_size


def human_readable(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)


def md5me(str):
	return hashlib.md5(str.encode('utf')).hexdigest()

def sha1me(str):
	return hashlib.sha1(str.encode('utf')).hexdigest()


# UPDATE - Feb 9, 2019 
# This is a potential vulnerability, go setup a separate machine to strip exif or do it some other way ;)
def clean_exif(path):
	try:
		subprocess.call(["exiftool", "-overwrite_original", "-all=", path])
	except Exception as e:
		raise e


def do_image_magic(req, filename):
	image = UploadedImage()
	image.album_id = ''
	image.username = req.user.get_username() if req.user.get_username() else 'Anonymous Upload' 
	image.image = filename
	image.is_private = False
	image.api_upload = False
	image.save()

	clean_exif(settings.MEDIA_ROOT+'/'+filename)

	# UPDATE - Feb 9, 2019 
	# This is a potential vulnerability do it some other way ;)
	try:
		subprocess.call(["convert", "-thumbnail", "150x150", settings.MEDIA_ROOT+'/'+filename, settings.THUMBNAIL_ROOT+'/'+filename])
	except Exception as e:
		raise e


def is_logged_in(request):
	return request.user.is_authenticated and request.user.is_active