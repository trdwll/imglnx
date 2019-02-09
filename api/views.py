"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.edit import View
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from PIL import Image

import os, subprocess

from imglnx.models import UploadedImage
from api.models import APIKeys

from imglnx.utilities import clean_exif, is_logged_in, human_readable


class DeleteKey(View):

	def get(self, request):
		if not is_logged_in(request):
			return redirect('login')
		
		return redirect('account:dashboard')

	def post(self, request):
		if not is_logged_in(request):
			return redirect('login')

		APIKeys.objects.filter(username=request.user.get_username(), api_key=request.POST.get('api_key', '')).delete()
		return redirect('account:dashboard')


class CreateKey(View):
	template_name = 'generate.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('login')

		return redirect('account:dashboard')

	def post(self, request):
		if not is_logged_in(request):
			return redirect('login')

		
		# only allow 5 API keys to be generated
		# TODO: add error messages on the render of the template
		cnt = APIKeys.objects.filter(username=request.user.get_username()).count()

		if cnt < 5:
			k = APIKeys(username=request.user.get_username(), api_key=get_random_string(length=32), upload_count=0)
			k.save()

		return redirect('account:dashboard')


@method_decorator(csrf_exempt, name='dispatch')
class ApiUpload(View):
	template_name = ''

	def get(self, request):
		return JsonResponse({"error": "You are not allowed to do GET requests here!"})

	def post(self, request):
		error = ''
		if request.FILES['images']:
			uploaded_image = request.FILES['images']
			fs = FileSystemStorage()
			name, extension = os.path.splitext(uploaded_image.name)
			upload_hash = get_random_string(length=settings.HASH_LENGTH) 

			# simple fix to avoid collisions
			if os.path.isfile(upload_hash + extension.lower()):
				upload_hash = get_random_string(length=settings.HASH_LENGTH+1)
			
			if uploaded_image.content_type in settings.IMAGE_TYPES and extension.lower() in settings.EXT:
				if uploaded_image.size <= settings.IMAGE_MAX_SIZE:
					filename = fs.save(upload_hash + extension.lower(), uploaded_image)
					#path = fs.url(filename) # returns /i/hash.ext

					try:
						# if user has api keys and if that key in the POST is on their account
						user_key = APIKeys.objects.filter(api_key=request.POST.get('auth_token', '')).values_list('username', flat=True).get()
						user_keycount = APIKeys.objects.filter(username=user_key).count()

						# check if the API key is valid then set the uploader username to the apikey owner
						if user_key and user_keycount >= 1: # the >= 1 is unnecessary since user_key is checking if the key is valid, but #yolo
							username = user_key # kinda bad naming, but returns the username of the auth_token/api_key owner ;)
						else:
							username = 'Anonymous Upload'
					except:
						username = 'Anonymous Upload'

					# check if request.user is a real user and check if that user is permitted to use the api key
					# if the request.user isn't a user then upload anonymously (without a key) and if the user exists, 
					# but the key doesn't for that user upload anonymously

					new_count = UploadedImage.objects.filter(api_upload_key=request.POST.get('auth_token', '')).count() + 1
					APIKeys.objects.filter(api_key=request.POST.get('auth_token', '')).update(upload_count=new_count)

					image = UploadedImage()
					image.username = username
					image.image = filename
					
					if username is not 'Anonymous Upload' and request.POST.get('private'):
						image.is_private = True
					else:
						image.is_private = False

					image.api_upload_key = request.POST.get('auth_token', '')
					image.api_upload = True
					image.save()

					clean_exif(settings.MEDIA_ROOT+'/'+filename)

					try:
						subprocess.call(["convert", "-thumbnail", "150x150", settings.MEDIA_ROOT+'/'+filename, settings.THUMBNAIL_ROOT+'/'+filename])
					except Exception as e:
						raise e

					return JsonResponse({"image": settings.MEDIA_URL+filename, "status": 200})
				else:
					error = 'File size is too large! Your size was ' + str(human_readable(uploaded_image.size)) + \
				' we only allow ' + str(human_readable(settings.IMAGE_MAX_SIZE)) + '.'
			else:
				error = 'Image type not allowed!'
		else:
			error = 'No image set to upload!'

		return JsonResponse({'error': error, "status": 403})
