from django.urls import path

from . import views

# Base url of the core app is '' (root)
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('legal/terms-of-service/', views.TermsOfServiceView.as_view(), name='terms-of-service'),

    # Test url for testing various items
    path('test/', views.TestView.as_view(), name='test'),
]
