from django.urls import path

from . import views

app_name = 'subscriptions'

# Root url of "roadmap" is 'roadmap/', defined in config.urls.py
urlpatterns = [
    path('', views.subscription_plans, name='subscription-plans')
]
