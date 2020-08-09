from django.urls import path

from .views import index, profile, BBLogoutView, BBLoginView, ChangeUserInfoView, BBPasswordChangeView, RegisterUserView, RegisterDoneView
from .views import user_activate, DeleteUserView, profile_pt_add, profile_pt_change, profile_pt_delete, detail, guest_pt_add, contain_comment

app_name = 'main'
urlpatterns = [
    path('', index, name = 'index'),
    path("add/", guest_pt_add, name = 'guest_pt_add'),
    path('<int:pk>/', detail, name = 'detail'),
    path('comment<int:pk>/', contain_comment, name = 'contain_comment'),
    path('accounts/register/', RegisterUserView.as_view(), name = 'register'),
    path('account/login/', BBLoginView.as_view(), name = 'login'),
    path('account/logout/', BBLogoutView.as_view(), name = 'logout'),
    path('accounts/profile/', profile, name = 'profile'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name = 'profile_delete'),
    path('accounts/register/actvate/<str:sign>/', user_activate, name = 'register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name = 'register_done'),
    path('accounts/profile/change/<int:pk>/', profile_pt_change, name = 'profile_pt_change'),
    path('accounts/profile/delete/<int:pk>/', profile_pt_delete, name = 'profile_pt_delete'),
    path('accounts/profile/add/', profile_pt_add, name = 'profile_pt_add'),   
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name = 'password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name = 'profile_change'), 
]

