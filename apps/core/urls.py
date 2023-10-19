from django.urls import path

from . import views

# Base url of the core app is '' (root)
urlpatterns = [
    path('', views.home, name='home'),
    path('legal/terms-of-service/', views.terms_of_service, name='terms-of-service'),

    path('blog/edit/89a77ec8-2a2f-4d1a-a573-322eb0372b32/upload_image/', views.upload_image, name='upload_image'),

    # Test url for testing various items
    path('test/', views.test, name='test'),
]
