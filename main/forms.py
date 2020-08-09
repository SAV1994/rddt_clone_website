from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import AdvUser, user_registrated, Pt, Comment, Comment_to_comment

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required = True, label = 'Адрес электронной почты')

	class Meta:
	    model = AdvUser
	    fields = ('email', 'first_name', 'last_name', 'telephone', 'anketa')		

class RegisterUserForm(forms.ModelForm):
	email = forms.EmailField(required = True, label = 'Адрес электронной почты')
	password1 = forms.CharField(label = 'Пароль', widget = forms.PasswordInput, 
		help_text = "Пароль не должен быть простым и содержать вашу персональную информацию. Ваш пароль должен содержать минимум 8 символов.")
	password2 = forms.CharField(label = 'Пароль (повторно)', widget = forms.PasswordInput,
		help_text = 'Ведите тот же самый пароль ещё раз для проверки')


	def clean_password(self):
		password1 = self.cleaned_data['password1']
		if password1:
			password_validation.validate_password(password1)
		return password1

	def clean(self):
		super().clean()
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 and password2 and password1 != password2:
			errors = {'password2': ValidationError('Ведённые пароли не совпадают', code = 'password_mismatch')}
			raise ValidationError(errors)

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False
		user.is_activated = False
		if commit:
			user.save()
		user_registrated.send(RegisterUserForm, instance = user)
		return user

	class Meta:
		model = AdvUser
		fields = ('username','email','password1','password2','first_name','last_name',)

class PtForm(forms.ModelForm):
	class Meta:
		model = Pt
		fields = '__all__'
		widgets = {'is_active': forms.HiddenInput, 'author': forms.HiddenInput}

class UserCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'pt': forms.HiddenInput, 'author': forms.HiddenInput}

class GuestCommentForm(forms.ModelForm):
	captcha = CaptchaField(label = 'ВВедите текст с картинки', error_messages = {'invalid': 'Неправильный текст'})

	class Meta:
		model = Comment
		fields = '__all__'
		widgets = {'pt': forms.HiddenInput, 'author': forms.HiddenInput, 'is_active': forms.HiddenInput}

class User_CommentForm(forms.ModelForm):
	class Meta:
		model = Comment_to_comment
		exclude = ('is_active',)
		widgets = {'key': forms.HiddenInput, 'pt': forms.HiddenInput, 'author': forms.HiddenInput}

class Guest_CommentForm(forms.ModelForm):
	captcha = CaptchaField(label = 'ВВедите текст с картинки', error_messages = {'invalid': 'Неправильный текст'})

	class Meta:
		model = Comment_to_comment
		fields = '__all__'
		widgets = {'key': forms.HiddenInput, 'author': forms.HiddenInput, 'is_active': forms.HiddenInput}

