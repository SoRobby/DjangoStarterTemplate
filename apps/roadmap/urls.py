from django.urls import path

from . import views

app_name = 'roadmap'

# Root url of "roadmap" is 'roadmap/', defined in config.urls.py
urlpatterns = [
    path('', views.roadmap, name='roadmap')
]
