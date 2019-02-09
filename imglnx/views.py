"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
import os, random
import urllib.request
import io

from django.shortcuts import (
	render, render_to_response, redirect, 
	HttpResponse, HttpResponseRedirect, reverse,
	get_list_or_404
)
from django.views.generic import View, UpdateView, ListView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile as TempFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from PIL import Image

from .models import UploadedImage, Album
from .forms import ContactForm #, NewAlbumForm

from .utilities import clean_exif, human_readable, do_image_magic



class LatestImagesView(ListView):
	model = UploadedImage
	template_name = 'latest.html'
	context_object_name = 'images'
	queryset = UploadedImage.objects.all().filter(is_private=False).order_by('-id')[:30]


def url_uploader(request):
	errors = ''
	if request.method == 'POST' and request.POST['image']:
		try:
			requested_url = urllib.request.urlopen(request.POST['image'])
		except:
			return JsonResponse({'errors': 'Site returned a 403, 404, or is down!'})

		if requested_url.getcode() == 200:
			# do head request here to get 
			mimetype = requested_url.headers['content-type']
			image_size = int(requested_url.headers['content-length'])
			fname = os.path.basename(request.POST['image']) 
			extension = os.path.splitext(fname)[1]

			if mimetype in settings.IMAGE_TYPES and extension.lower() in settings.EXT:
				if image_size <= settings.IMAGE_MAX_SIZE:

					# check file extensions
					# if any(settings.EXT in fname for settings.EXT in settings.EXT):
					# 	print('yes')
					# else:
					# 	print('no')

					# this is hacky, but it'll do for now
					if '?' in fname or ':' in fname:
						extension = '.jpg'
					# 	extension = os.path.splitext(fname.split('?')[0])[1]
					#else:
					#	extension = os.path.splitext(fname)[1]

					
					fs = FileSystemStorage()
					upload_hash = get_random_string(length=settings.HASH_LENGTH)

					# simple fix to avoid collisions
					if os.path.isfile(upload_hash + extension.lower()):
						upload_hash = get_random_string(length=settings.HASH_LENGTH+1)

					filename = fs.save(upload_hash + extension.lower(), io.BytesIO(requested_url.read()))
					#path = fs.url(filename)   # returns /i/hash.ext

					try:
						if Image.open(settings.MEDIA_ROOT+'/'+filename):
							pass
					except Exception as e:
						os.remove(settings.MEDIA_ROOT+'/'+filename) # delete the corrupt/invalid image
						return JsonResponse({"image": "", "status": 403, "error": "Not a valid image! Aka the image is incomplete, altered in someway, or it's just not an image."})

					do_image_magic(request, filename)

					return JsonResponse({"image": settings.MEDIA_URL+filename, "status": 200, "error": False})
				else:
					errors = 'Image is too large!'	
			else:
				errors = 'Image type not allowed!' 

	return render(request, 'home.html', {'errors': errors})


def uploader(request):
	errors = ''
	if request.method == 'POST' and request.FILES['images']:

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

				# to write webm we have to write by chunks like tmpfile fs.save doesn't work for webm for some reason

				try:
					if Image.open(settings.MEDIA_ROOT+'/'+filename):
						pass
				except Exception as e:
					os.remove(settings.MEDIA_ROOT+'/'+filename) # delete the corrupt/invalid image
					return JsonResponse({"image": "", "status": 403, "error": "Not a valid image! Aka the image is incomplete, altered in someway, or it's just not an image."})

				do_image_magic(request, filename)

				return JsonResponse({"image": settings.MEDIA_URL+filename, "status": 200, "error": False})
			else:
				errors = 'File size is too large! Your size was ' + str(human_readable(uploaded_image.size)) + \
				' we only allow ' + str(human_readable(settings.IMAGE_MAX_SIZE)) + '.'
		else:
			errors = 'File type isn\'t allowed!'

	return JsonResponse({"image": "", "status": 403, "error": errors})


class ContactView(View):
	form_class = ContactForm
	template_name = 'contact.html'

	def get(self, request):
		form = self.form_class(None)

		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = ContactForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			reason = form.cleaned_data['reason']
			message = form.cleaned_data['message']
			form.save()

			return redirect('contact-thanks')

		return render(request, self.template_name, {'form': form, 'errors': form.errors})


class NewAlbumView(View):
#	form_class = NewAlbumForm
	template_name = 'imglnx/album_form.html'

	def get(self, request):
		form = self.form_class(None)
		images = UploadedImage.objects.filter(username=request.user.get_username())

		return render(request, self.template_name, {'form': form, 'images': images})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			album = form.save(commit=False)
			album.album_title = form.cleaned_data['title']
			album.username = request.user
			for selected in request.POST.getlist('addtoalbum'):
				album.stored_images += selected + ','
			album.save()

		return redirect('home')


"""
Error pages
"""
def handler400(request):
	return render(request, 'error_pages/400.html', status=400)

def handler403(request):
	return render(request, 'error_pages/403.html', status=403)

def handler404(request):
	return render(request, 'error_pages/404.html', status=404)

def handler500(request):
	return render(request, 'error_pages/500.html', status=500)