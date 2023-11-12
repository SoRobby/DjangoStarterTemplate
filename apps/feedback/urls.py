from django.urls import path

from . import views

app_name = 'feedback'

# Root url of "feedback" is 'feedback/', defined in config.urls.py
urlpatterns = [
    path('submit/', views.submit_feedback, name='submit-feedback')
]
