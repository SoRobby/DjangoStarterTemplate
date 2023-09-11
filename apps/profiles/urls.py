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
from django.urls import path

from apps.profiles import views

app_name = 'profiles'

# Base url of the profile app is 'profile' (root)
urlpatterns = [
    # Account profile urls
    path('profiles/<str:username>/', views.ProfileView.as_view(), name='profile'),

    # Account profile edit
    path('settings/general/', views.ProfileEditGeneralView.as_view(), name='settings-general'),

    path('settings/security/', views.ProfileEditSecurityView.as_view(), name='settings-security'),

    path('settings/security/change-email/', views.profile_edit_security_change_email,
         name='settings-security-change-email'),

    path('settings/notifications/', views.ProfileEditNotificationsView.as_view(), name='settings-notifications'),

    path('settings/support/', views.ProfileEditSupportView.as_view(), name='settings-support'),

    # Send support message
    path('support/send-message/', views.profile_edit_support_send_message, name='support-send-message'),

]
