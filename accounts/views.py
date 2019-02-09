"""
BSD 3-Clause License

Copyright (c) 2017-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import UpdateView, View
from django.views.generic import ListView
from django.shortcuts import (
	render, HttpResponse, redirect, 
	HttpResponseRedirect, get_object_or_404, get_list_or_404
)
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from wsgiref.util import FileWrapper

from accounts.forms import (
	RegistrationForm, UpdateProfileForm, 
	#RecoverAccountForm, 
	#RecoverAccountResetForm, 
	LoginForm, 
	#RecoveryCodeSetupForm, 
	User
)
#from accounts.models import UserProfile
from imglnx.models import UploadedImage, Album
from api.models import APIKeys
from imglnx.utilities import sha1me, is_logged_in

import os
import tempfile
import datetime
import zipfile
from os.path import basename


class DeleteAccountView(View):
	template_name = 'accounts/dashboard.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		return render(request, self.template_name)

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		try:
			u = User.objects.get(username=request.user.get_username())
			if u is not None:
				# delete thumbnails
				images = UploadedImage.objects.all().filter(username=request.user.get_username())
				if images:
					for img in images:
						if os.path.isfile(settings.THUMBNAIL_ROOT+'/'+str(img.image)):
							os.remove(settings.THUMBNAIL_ROOT+'/'+str(img.image))

				UploadedImage.objects.filter(username=request.user.get_username()).delete()
				APIKeys.objects.filter(username=request.user.get_username()).delete()
				Album.objects.filter(username=request.user.get_username()).delete()
				u.delete()
		except User.DoesNotExist:
			return render(request, self.template_name, {'errors': 'The username doesn\'t exist!'})

		return render(request, self.template_name, {'errors': 'Successfully deleted your account!'})

		
class DownloadView(View):
	template_name = 'accounts/dashboard.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		random_hash = sha1me(request.session.session_key[7:-7])

		return redirect(settings.ARCHIVES_URL+request.user.get_username()+'-'+random_hash+'-archive.zip')

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		random_hash = sha1me(request.session.session_key[7:-7])

		images = UploadedImage.objects.all().filter(username=request.user.get_username())

		ZipFile = zipfile.ZipFile(settings.ARCHIVES_ROOT+'/'+request.user.get_username()+'-'+random_hash+'-archive.zip', 'w')

		for img in images:
			i = os.path.basename(str(img.image))
			ZipFile.write(settings.MEDIA_ROOT+'/'+i, basename(settings.MEDIA_ROOT+'/'+i), compress_type=zipfile.ZIP_DEFLATED)

		return render(request, self.template_name)


# user dashboard 
class UpdateProfileView(View):
	form_class = UpdateProfileForm
	template_name = 'accounts/dashboard.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		images = UploadedImage.objects.all().filter(username=request.user.get_username())
		albums = Album.objects.all().filter(username=request.user.get_username())
		api_keys = APIKeys.objects.all().filter(username=request.user.get_username())

		form = UpdateProfileForm(request.POST, instance=request.user, user=request.user)
		return render(request, self.template_name, {'form': form, 'images': images, 'albums': albums, 'api_keys': api_keys })

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		form = UpdateProfileForm(request.POST, instance=request.user, user=request.user)
		if form.is_valid():
			user = form.save(commit=False)
			passwordcur = form.cleaned_data['passwordcur']
			passwordnew = form.cleaned_data['passwordnew']
			passwordconf = form.cleaned_data['passwordconf']

			valid = User.objects.get(username=request.user.get_username()).check_password(passwordcur)
			if valid:
				#user.email = form.cleaned_data['email']
				if str(passwordnew) == str(passwordconf) and (len(passwordnew) >= 8 and len(passwordconf) >= 8):
					user.set_password(passwordnew)
					newauth = passwordnew
				else:
					user.set_password(passwordcur)
					newauth = passwordcur

				# update the email on the UserProfile also
				#f = UserProfile.objects.get(user=request.user.pk)
				#f.email = form.cleaned_data['email']
				#f.save()
				form.save()

				if user is not None and user.is_active:
					login(request, authenticate(username=request.user.get_username(), password=newauth))
					return render(request, self.template_name, {'form': form})

				return render(request, self.template_name, {'form': form, 'errors': 'It looks like your account doesn\'t exist, please contact support!'})
			return render(request, self.template_name, {'form': form, 'errors': 'Invalid password, try again!'})

		return render(request, self.template_name, {'form': form, 'errors': 'Invalid information, try again!'})


class ChangeImageVisibility(View):
	template_name = 'accounts/images.html'

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')
			
		img = request.POST['image']
		image = UploadedImage.objects.get(image=img, username=request.user.get_username())

		if image:
			if image.is_private == 1:
				image.is_private = 0
			else:
				image.is_private = 1
				
			image.save()

		return redirect('account:images')


class ImagesView(View):
	template_name = 'accounts/images.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		TOTAL_ON_PAGE = 30

		try:
			TOTAL_ON_PAGE = int(request.GET.get('num', 30))
		except ValueError:
			print("Input wasn't an integer - defaulting to 30")

		if TOTAL_ON_PAGE > 1000:
			TOTAL_ON_PAGE = 1000

		username = request.user.get_username()
		images = UploadedImage.objects.all().filter(username=username)
		albums = Album.objects.all().filter(username=username)

		if len(images) > TOTAL_ON_PAGE and TOTAL_ON_PAGE > 1:
			page = request.GET.get('page', 1)

			paginator = Paginator(images, TOTAL_ON_PAGE)
			try:
				images = paginator.page(page)
			except PageNotAnInteger:
				images = paginator.page(1)
			except EmptyPage:
				images = paginator.page(paginator.num_pages)

			return render(request, self.template_name, {'images': images, 'pagination': paginator, 'albums': albums, 'TOTAL_ON_PAGE': TOTAL_ON_PAGE})

		if len(images) <= 0:
			return render(request, self.template_name, 
				{'errors': 'You don\'t have any images uploaded under your account name <strong>'+username+'</strong>! Go to <a href="/">Home</a> to begin uploading to your account!'}
			)

		return render(request, self.template_name, {'images': images, 'albums': albums})

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		if request.POST['images[]']:
			if request.POST['del']:
				for img in request.POST.getlist('images[]'):
					UploadedImage.objects.get(image=img, username=request.user.get_username()).delete()

		return render(request, self.template_name)


class DeleteAlbum(View):
	template_name = 'accounts/albums.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		return render(request, self.template_name)

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		if request.POST['album']:
			Album.objects.get(album_id=request.POST['album'], username=request.user.get_username()).delete()

		return render(request, self.template_name)


class RemoveImageAlbum(View):
	template_name = 'accounts/view_album.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		return render(request, self.template_name)

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		if request.POST['image']:
			img = UploadedImage.objects.get(image=request.POST['image'], username=request.user.get_username())

			if img:
				img.album_id = ''
				img.save()

		return render(request, self.template_name)


class AddToAlbum(View):
	template_name = 'accounts/images.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		return render(request, self.template_name)

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		if request.POST['images[]']:
			if request.POST['alb']:
				for img in request.POST.getlist('images[]'):
					image = UploadedImage.objects.get(image=img, username=request.user.get_username())
					album = Album.objects.get(album_id=request.POST['alb'], username=request.user.get_username())

					if image and album:
						image.album_id = album.pk
						image.save()

		return render(request, self.template_name)


class AlbumsView(View):
	template_name = 'accounts/albums.html'

	def get(self, request):
		if not is_logged_in(request):
			return redirect('home')

		TOTAL_ON_PAGE = 30

		try:
			TOTAL_ON_PAGE = int(request.GET.get('num', 30))
		except ValueError:
			print("Input wasn't an integer - defaulting to 30")

		if TOTAL_ON_PAGE > 1000:
			TOTAL_ON_PAGE = 1000

		albums = Album.objects.all().filter(username=request.user.get_username())

		if len(albums) > TOTAL_ON_PAGE and TOTAL_ON_PAGE > 1:
			page = request.GET.get('page', 1)

			paginator = Paginator(albums, TOTAL_ON_PAGE)
			try:
				albums = paginator.page(page)
			except PageNotAnInteger:
				albums = paginator.page(1)
			except EmptyPage:
				albums = paginator.page(paginator.num_pages)

			return render(request, self.template_name, {'pagination': paginator, 'albums': albums, 'TOTAL_ON_PAGE': TOTAL_ON_PAGE})

		if len(albums) <= 0:
			errors = 'You don\'t have any albums under your account name <strong>' + request.user.get_username() + '</strong>! Create an album below, then go to <a href="'+reverse('account:images')+'">Images</a> and select images to add to an album!'
			return render(request, self.template_name, {'errors': errors})

		return render(request, self.template_name, {'albums': albums})

	def post(self, request):
		if not is_logged_in(request):
			return redirect('home')

		if request.POST['title']:
		 	album = Album()
		 	album.title = request.POST['title']
		 	album.username = request.user.get_username()
		 	album.album_id = get_random_string(length=8)
		 	album.save()

		return render(request, self.template_name)


class ViewAlbumView(View):
	template_name = 'accounts/view_album.html'

	def get(self, request, album_id):

		TOTAL_ON_PAGE = 30

		try:
			TOTAL_ON_PAGE = int(request.GET.get('num', 30))
		except ValueError:
			print("Input wasn't an integer - defaulting to 30")

		if TOTAL_ON_PAGE > 1000:
			TOTAL_ON_PAGE = 1000

		album = get_object_or_404(Album.objects.all().filter(album_id=album_id)) 
		images = get_list_or_404(UploadedImage.objects.all().filter(
			album_id=Album.objects.filter(album_id=album_id).values_list('pk', flat=True)))

		if len(images) > TOTAL_ON_PAGE and TOTAL_ON_PAGE > 1:
			page = request.GET.get('page', 1)

			paginator = Paginator(images, TOTAL_ON_PAGE)
			try:
				images = paginator.page(page)
			except PageNotAnInteger:
				images = paginator.page(1)
			except EmptyPage:
				images = paginator.page(paginator.num_pages)

			if album and images:
				username = album.username
				if album.is_private:
					username = 'Anonymous Upload'
				
				return render(request, self.template_name, 
					{'pagination': paginator, 'album': album, 'images': images, 'username': username, 
					'TOTAL_ON_PAGE': TOTAL_ON_PAGE})

			if len(images) <= 0:
				return render(request, self.template_name, {'errors': 'nope'})

		return render(request, self.template_name, {'images': images, 'album': album})

class LoginUser(View):
	template_name = 'accounts/auth/login.html'

	def get(self, request):
		if is_logged_in(request):
			return redirect('home')
		
		return render(request, self.template_name, {'form': LoginForm()})

	def post(self, request):
		if is_logged_in(request):
			return redirect('home')

		form = LoginForm(request.POST)
		if form.is_valid():
			# username = request.POST['username']
			# password = request.POST['password']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)
			if user is not None and user.is_active:
				login(request, user)
				return redirect('account:dashboard')

			error = 'Account doesn\'t exist (username/email are invalid or the account isn\'t registered) or the account is inactive/banned.'
		else:
			error = 'Invalid captcha, try again.'
	
		return render(request, 'accounts/auth/login.html', {'form': form, 'error': error})


class RegisterUser(View):
	template_name = 'accounts/auth/register.html'

	def get(self, request):
		if is_logged_in(request):
			return redirect('home')

		return render(request, 'accounts/auth/register.html', {'form': RegistrationForm()})

	def post(self, request):
		if is_logged_in(request):
			return redirect('home')

		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			# add the email on the UserProfile also
			u = User.objects.get(username=form.cleaned_data['username'])
			#f = UserProfile.objects.create(user=u)
			#f.save()
			return redirect('login')		
		else:
			error = 'Invalid captcha, try again.'
		
		return render(request, 'accounts/auth/register.html', {'form': form, 'error': error})

	
# class forgot_user(View):
# 	template_name = 'accounts/auth/forgot.html'

# 	def get(self, request):
# 		if is_logged_in(request):
# 			return redirect('home')

# 		return render(request, self.template_name, {'form': RecoverAccountForm()})

# 	def post(self, request):
# 		if is_logged_in(request):
# 			return redirect('home')

# 		form = RecoverAccountForm(request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data['username']
# 			email = form.cleaned_data['email']
# 			recovery_code = form.cleaned_data['recovery_key']

# 			# check if the user is valid
# 			# try/catch instead of get_object_or_404
# 			try:
# 				u = User.objects.get(username=username, email=email)
# 			except:
# 				return render(request, 'accounts/auth/forgot.html', {'form': form, 
# 					'error': 'Invalid username or email. Try again or contact support.'})

# 			if u:
# 				prof = UserProfile.objects.get(user=u.pk)
# 				if prof:
# 					if recovery_code == prof.recovery_key:
# 						request.session['jkbh1jkh23jkhjasdjkhasd'] = 1 # to verify elsewhere
# 						request.session['ulkj2kl3j1z'] = username # username
# 						request.session['knadshdnmndfjahsd'] = email # email
# 						return redirect('forgot-reset')

# 					error = 'Your recovery key is invalid.'
# 				error = 'Something went wrong while verifying your recovery key! Please contact support!'
# 			#error = 'Invalid username or email. Try again or contact support.'
# 		else:
# 			error = 'Invalid captcha, try again.'
		
# 		return render(request, 'accounts/auth/forgot.html', {'form': form, 'error': error})


# class forgot_user_reset(View):
# 	template_name = 'accounts/auth/forgot_reset.html'

# 	def get(self, request):
# 		if is_logged_in(request) or not request.session.get('jkbh1jkh23jkhjasdjkhasd', ''):
# 			return redirect('home')

# 		return render(request, self.template_name, {'form': RecoverAccountResetForm()})

# 	def post(self, request):
# 		if is_logged_in(request) or not request.session.get('jkbh1jkh23jkhjasdjkhasd', ''):
# 			return redirect('home')

# 		form = RecoverAccountResetForm(request.POST)
# 		if form.is_valid():
# 			pwd1 = form.cleaned_data['password1']
# 			pwd2 = form.cleaned_data['password2']
# 			username = request.session.get('ulkj2kl3j1z', '')
# 			email = request.session.get('knadshdnmndfjahsd', '')

# 			user = User.objects.get(username=username, email=email)
# 			if str(pwd1) == str(pwd2) and (len(pwd1) >= 8 and len(pwd2) >= 8):
# 				# get user obj
# 				user.set_password(pwd1)
# 				user.save()
# 				if user is not None and user.is_active:
# 					for k in list(request.session.keys()):
# 						del request.session[k]
					
# 					return redirect('login')
# 					#login(request, authenticate(username=user.username, password=pwd1))

# 				error = 'Invalid account, please press the back button and restart the recovery process.'
# 			error = 'Password length isn\'t long enough or the passwords don\'t match.'
# 		else:
# 			error = 'Something went wrong with the form. Please resubmit!'
		
# 		return render(request, self.template_name, {'form': form, 'error': error})


# class SetRecoveryCode(View):
# 	template_name = 'accounts/auth/recovery_key.html'

# 	def get(self, request):
# 		if not is_logged_in(request):
# 			return redirect('home')

# 		return render(request, self.template_name, {'form': RecoveryCodeSetupForm()})

# 	def post(self, request):
# 		if not is_logged_in(request):
# 			return redirect('home')
			
# 		form = RecoveryCodeSetupForm(request.POST)
# 		if form.is_valid():
# 			user = UserProfile.objects.get(user=request.user.pk)
# 			password = form.cleaned_data['password1']
# 			key = form.cleaned_data['recovery_key']

# 			if user is not None and authenticate(username=request.user.get_username(), password=password):
# 				if key is not '':
# 					user.recovery_key = key
# 					user.save()
# 					return redirect('account:dashboard')

# 				error = 'Key is empty, please set something and try again.'
# 			error = 'Password is invalid, try again.'
# 		else:
# 			error = 'Something went wrong, try again.'

# 		return render(request, self.template_name, {'form': form, 'error': error})