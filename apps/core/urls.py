from django.urls import path

from . import views

# Base url of the core app is '' (root)
urlpatterns = [
    path('', views.home, name='home'),
    path('legal/terms-of-service/', views.terms_of_service, name='terms-of-service'),

    # Test url for testing various items
    path('test/', views.test, name='test'),
]
