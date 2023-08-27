from django.urls import path

from . import views

# Base url of the main app is '' (root)
urlpatterns = [
    path('', views.home, name='home'),
    # path('submit-feedback/', views.submit_feedback, name='submit-feedback'),
    path('legal/terms-of-service/', views.terms_of_service, name='terms-of-service'),
]
