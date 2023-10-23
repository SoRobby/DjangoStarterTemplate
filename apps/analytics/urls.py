from django.urls import path

from . import views

app_name = 'analytics'

# Root url of "analytics" is 'analytics/', defined in config.urls.py
urlpatterns = [
    path('onload-endpoint/', views.analytics_onload_endpoint, name='onload-endpoint'),
    path('beforeunload-endpoint/', views.analytics_beforeunload_endpoint, name='beforeunload-endpoint'),
]
