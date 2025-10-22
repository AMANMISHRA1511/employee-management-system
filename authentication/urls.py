from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/auth/login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('two-factor/', views.two_factor_view, name='two_factor'),
    path('resend-code/', views.resend_code_view, name='resend_code'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),
    path('toggle-2fa/', views.toggle_2fa_view, name='toggle_2fa'),
]