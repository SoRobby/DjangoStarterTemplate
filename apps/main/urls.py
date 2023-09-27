from django.urls import path

from . import views

# Base url of the main app is '' (root)
urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('legal/terms-of-service/', views.terms_of_service, name='terms-of-service'),
]
