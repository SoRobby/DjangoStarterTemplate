from django.urls import path

from . import views

app_name = 'feedback'

# Base url of the core app is '' (root)
urlpatterns = [
    path('feedback/submit/', views.submit_feedback, name='submit-feedback')
]
