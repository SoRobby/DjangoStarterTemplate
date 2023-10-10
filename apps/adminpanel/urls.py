from django.urls import path

from . import views

app_name = 'adminpanel'

# Base url of the profile app is 'adminpanel' (/adminpanel/)
urlpatterns = [
    path('components/', views.AdminPanelComponentsView.as_view(), name='components'),
]
