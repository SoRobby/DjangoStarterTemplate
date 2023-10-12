from django.urls import path

from . import views

app_name = 'analytics'

# Base url of the profile app is 'analytics' (root)
urlpatterns = [
    path('analytics/onload-endpoint/', views.analytics_onload_endpoint, name='onload-endpoint'),
    path('analytics/beforeunload-endpoint/', views.analytics_beforeunload_endpoint, name='beforeunload-endpoint'),
]
