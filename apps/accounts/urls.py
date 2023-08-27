"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts import views

# app_name = 'accounts'

# Base url of the accounts app is '' (root)
urlpatterns = [
    # Account generic functions - login, logout and register
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete-account/', views.delete_account_view, name='delete-account'),

    # Verify account email

    # path('verify/<user>/send-verification/', views.send_verification_email, name='send-verification-email'),

    path('verify/token/<str:token>/', views.verify_email, name='verify-email'),
    path('verify/send/<str:username>/', views.send_verification_email_view, name='send-verification-email'),

    # Account password reset / change urls
    # https://github.com/django/django/blob/master/django/contrib/auth/views.py
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change/password_change.html'), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change/password_change_done.html'), name='password_change_done'),

    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset/password_reset_form.html', html_email_template_name='accounts/password_reset/password_reset_email.html'), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/success/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
