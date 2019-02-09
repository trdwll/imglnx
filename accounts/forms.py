"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django import forms
from django.contrib.auth.models import User
#from . models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

class RegistrationForm(UserCreationForm):
	captcha = CaptchaField()
	username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			min_length=3, label='Username', required=True, help_text='Choose a unique username to login with.')
#	email = forms.CharField(
#			widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}), 
#			min_length=5, label='Email Address', required=True, 
#			help_text='Feel free to use a fake or even a disposable email address. We don\'t verify the email, it\'s only used to recover the account or if we need to contact you.')
	
	placeholder = 'Must be at least 8 characters'
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
		min_length=8, label='Password', required=True, help_text='Enter your password!')
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
		min_length=8, label='Confirm Password', required=True, help_text='Confirm your password!')
	
	class Meta:
		model = User
		fields = [
			'username',
		#	'email',
			'password1',
			'password2',
			'captcha'
		]

class LoginForm(forms.Form):
	username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			min_length=3, label='Username', required=True)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Must be at least 8 characters'}), 
		min_length=8, label='Password', required=True, help_text='Enter your password!')
	captcha = CaptchaField()

	class Meta:
		fields = [
			'username',
			'password',
			'captcha'
		]


class UpdateProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(UpdateProfileForm, self).__init__(*args, **kwargs)
		#self.fields['username'] = forms.CharField(widget=forms.TextInput(attrs={'value': user}))
		userinfo = User.objects.get(username=user)
		#useremail = userinfo.email
		#self.fields['email'] = forms.CharField(
		#	widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'value': useremail}), 
		#	min_length=5, label='Email Address', required=True)
	
	placeholder = 'Must be at least 8 characters'
	passwordcur = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
		min_length=8, label='Current Password', required=True, help_text='Enter your current password to verify the change.')
	passwordnew = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
		min_length=8, label='New Password', required=False, help_text='Make sure your new password isn\'t use anywhere else.')
	passwordconf = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
		min_length=8, label='Confirm New Password', required=False, help_text='Confirm your new password!')

	class Meta:
		model = User
		fields = [
		#	'username',
			'passwordcur',
#			'email',
			'passwordnew',
			'passwordconf'
		]


# class RecoverAccountForm(forms.ModelForm):
# 	captcha = CaptchaField()

# 	username = forms.CharField(
# 		widget=forms.TextInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Enter your Username.'}), 
# 		min_length=4, label='Username', required=True)
# 	email = forms.CharField(
# 		widget=forms.EmailInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Enter your Email.'}), 
# 		min_length=5, label='Email', required=True)
# 	recovery_key = forms.CharField(
# 		widget=forms.TextInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Enter your recovery key.'}), 
# 		min_length=5, label='Recovery Key', required=True)

# 	class Meta:
# 		model = UserProfile
# 		fields = [
# 			'username',
# 			'email',
# 			'recovery_key',
# 			'captcha'
# 		]

# class RecoverAccountResetForm(forms.ModelForm):
# 	placeholder = 'Must be at least 8 characters'
# 	password1 = forms.CharField(
# 		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
# 		min_length=8, label='New Password', required=True, help_text='Make sure your new password isn\'t use anywhere else.')
# 	password2 = forms.CharField(
# 		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': placeholder}), 
# 		min_length=8, label='Confirm New Password', required=True, help_text='Confirm your new password!')

# 	class Meta:
# 		model = User
# 		fields = [
# 			'password1',
# 			'password2'
# 		]


# class RecoveryCodeSetupForm(forms.Form):
# 	password1 = forms.CharField(
# 		widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Must be at least 8 characters'}), 
# 		min_length=8, label='Current Password', required=True, help_text='Your current password')
# 	recovery_key = forms.CharField(
# 		widget=forms.TextInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Enter your Recovery Key.'}), 
# 		min_length=4, label='Recovery Key', required=True)

# 	class Meta:
# 		fields = [
# 			'password1',
# 			'recovery_key'
# 		]