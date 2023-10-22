from django.urls import path

from . import views

app_name = 'blog'

# Base url of the profile app is 'profile' (root)
urlpatterns = [
    # Account profile urls
    # URL of blog post by slug
    path('articles/', views.article_list, name='article-list'),

    # path is /blog/<str:slug>/
    # path('posts/<str:slug>/', views.post, name='post'),
    # TODO - NEED TO FIX URL FOR POSTS -> ARTICLES
    path('posts/<str:slug>/', views.PostDetailView.as_view(), name='post'),

    # path is /blog/edit/create-post/

    path('edit/create/', views.create_article, name='create-article'),
    path('edit/<str:uuid>/', views.edit_article, name='edit-article'),
    path('edit/<str:uuid>/upload-article-image', views.upload_article_image, name='upload-article-image'),

    path('edit/<str:uuid>/delete/', views.delete_article, name='delete-article'),

]
