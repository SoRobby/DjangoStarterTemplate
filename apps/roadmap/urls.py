from django.urls import path

from . import views

app_name = 'roadmap'

# Base url is 'roadmap' (root) - defined in config.urls.py
urlpatterns = [
    # Account profile urls
    # URL of blog post by slug
    path('', views.roadmap, name='roadmap'),



]
