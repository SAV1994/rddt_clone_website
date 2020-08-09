from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification, get_timestamp_path

class AdvUser(AbstractUser):
	is_activated = models.BooleanField(default = True, db_index = True, verbose_name = 'Прошел активацию?')
	telephone = models.CharField(max_length =12, verbose_name = 'Номер телефона')
	anketa = models.TextField(verbose_name = 'О себе')

	class Meta(AbstractUser.Meta):
		pass

class Pt(models.Model):

	title = models.CharField(max_length = 50, verbose_name = 'Заголовок')
	author = models.CharField(max_length = 50, verbose_name = 'Автор')
	content = models.TextField(verbose_name = 'Статья')
	created_at = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликовано')
	image = models.ImageField(blank = True, upload_to = get_timestamp_path, verbose_name = 'Изображение')
	is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить на экран?')
	
	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = "Статьи"
		ordering = ['-created_at']
	
user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)

class Comment(models.Model):
	pt = models.ForeignKey(Pt, on_delete = models.CASCADE, verbose_name = 'Статья')
	author = models.CharField(max_length = 50, db_index = True, verbose_name = 'Автор')
	content = models.TextField(verbose_name = 'Комментарий')
	is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить на экран?')
	created_at = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликован')

	class Meta:
		verbose_name_plural = 'Комментарии'
		verbose_name = 'Комментарий'
		ordering = ['-created_at']

class Comment_to_comment(models.Model):
	key = models.ForeignKey(Comment, on_delete = models.CASCADE)
	author = models.CharField(max_length = 50, verbose_name = 'Автор')
	content = models.TextField(verbose_name = 'Комментарий')
	is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить на экран?')
	created_at = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликован')

	class Meta:
		verbose_name_plural = 'Комментарии 2-го порядка'
		verbose_name = 'Комментарий 2-го порядка'
		ordering = ['-created_at']


