from django.urls import path

from . import views

app_name = 'blog'

# Base url of the profile app is 'profile' (root)
urlpatterns = [
    # Account profile urls
    # URL of blog post by slug
    path('posts/', views.post_list, name='post-list'),
    
    # path is /blog/<str:slug>/
    path('posts/<str:slug>/', views.post, name='post'),

    # path is /blog/edit/create-post/
    path('create-post/', views.create_post, name='create-post'),
    path('edit/<str:uuid>/', views.edit_post, name='edit-post'),
]