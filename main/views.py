from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator

from .models import AdvUser, Pt,  Comment, Comment_to_comment
from .forms import ChangeUserInfoForm, RegisterUserForm, PtForm, UserCommentForm, GuestCommentForm, User_CommentForm, Guest_CommentForm  
from .utilities import signer

def index (request):
	pts = Pt.objects.filter(is_active = True)
	paginator = Paginator(pts, 2)

	page_number = request.GET.get('page', 1)
	page = paginator.get_page(page_number)

	context = {'pts': page}
	return render(request, 'main/index.html', context)

class BBLoginView(LoginView):
	template_name = 'main/login.html'

@login_required
def profile(request):
	pts = Pt.objects.filter(author = request.user.username)
	context = {'pts': pts}
	return render(request, 'main/profile.html', context)

class BBLogoutView(LoginRequiredMixin, LogoutView):
	template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	model = AdvUser
	template_name = 'main/change_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('main:profile')
	
	def dispatch(self, request, *args, **kwargs):
		self.user_id =request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset = None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
	template_name = 'main/password_change.html'
	success_url = reverse_lazy('main:password_change')
	success_message = 'Пароль успешно изменён'
	
class RegisterUserView(CreateView):
	model = AdvUser
	template_name = 'main/register_user.html'
	form_class = RegisterUserForm
	success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
	template_name = 'main/register_done.html'

def user_activate(request, sign):
	try:
		username = signer.unsign(sign)
	except BadSignature:
		return render(request, 'main/bad_signature.html')
	user = get_object_or_404(AdvUser, username = username)
	if user.is_activated:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.is_activated = True
		user.save()
	return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
	model = AdvUser
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:index')

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request)
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset = None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)


@login_required
def profile_pt_add(request):
	if request.method == 'POST':
		form = PtForm(request.POST, request.FILES, initial = {'author': request.user.username})
		if form.is_valid():
			pt = form.save()
			messages.add_message(request, messages.SUCCESS, 'Статья добавлена')
			return redirect('main:profile_pt_add')
	else:
		form = PtForm(initial = {'author': request.user.username})
	context = {'form': form}
	return render(request, 'main/profile_pt_add.html', context)	

@login_required
def profile_pt_change(request, pk):
	pt = get_object_or_404(Pt, pk = pk)
	if request.method == 'POST':
		form = PtForm(request.POST, request.FILES, instance = pt)
		if form.is_valid():
			pt = form.save()
			return redirect('main:profile')
	else:
		form = PtForm(instance = pt)
		context = {'form':form}
		return render(request, 'main/profile_pt_change.html', context)

@login_required
def profile_pt_delete(request, pk):
	pt = get_object_or_404(Pt, pk = pk)
	if request.method == 'POST':
		pt.delete()
		return redirect('main:profile')
	else:
	    context = {'pt': pt}
	    return render(request, 'main/profile_pt_delete.html', context)

def detail (request, pk):
	pt = Pt.objects.get(pk = pk)
	comments = Comment.objects.filter(pt = pk, is_active = True)
	initial = {'pt': pt.pk}
	if request.user.is_authenticated:
		initial['author'] = request.user.username
		form_class = UserCommentForm
	else:
		initial['author'] = "Незарегистрированный пользователь"
		initial['is_active'] = False
		form_class = GuestCommentForm
	form = form_class(initial = initial)
	if request.method == 'POST':
		c_form = form_class(request.POST)
		if c_form.is_valid():
			c_form.save()
			messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
		else:
			form = c_form
			messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
	context = {'pt': pt, 'comments': comments, 'form': form}
	return render(request, 'main/detail.html', context)

def guest_pt_add(request):
	if request.method == 'POST':
		form = PtForm(request.POST, request.FILES, initial = {'author': 'Незарегистрированный пользователь', 'is_active': False})
		if form.is_valid():
			pt = form.save()
			messages.add_message(request, messages.SUCCESS, 'Статья будет отображена на сайте после прохождения процесса модерации')
			return redirect('main:guest_pt_add')
	else:
		form = PtForm(initial = {'author': 'Незарегистрированный пользователь', 'is_active': False})
	context = {'form': form}
	return render(request, 'main/guest_pt_add.html', context)

def contain_comment (request, pk):
	comment = Comment.objects.get(pk = pk)
	coms = Comment_to_comment.objects.filter(key_id = pk, is_active = True)
	initial = {'comment': comment.pk}
	if request.user.is_authenticated:
		initial['author'] = request.user.username
		initial['key'] = comment.pk
		form_class = User_CommentForm
	else:
		initial['author'] = "Незарегистрированный пользователь"
		initial['is_active'] = False
		initial['key'] = comment.pk
		form_class = Guest_CommentForm
	form = form_class(initial = initial)
	if request.method == 'POST':
		c_form = form_class(request.POST)
		if c_form.is_valid():
			c_form.save()
			messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
		else:
			form = c_form
			messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
	context = {'coms': coms, 'comment': comment, 'form': form}
	return render(request, 'main/contain_comment.html', context)	