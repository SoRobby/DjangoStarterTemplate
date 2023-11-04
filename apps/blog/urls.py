from django.urls import path

from . import views

app_name = 'blog'

# Root url of "blog" is 'blog/', defined in config.urls.py
urlpatterns = [
    # Articles
    path('articles/', views.article_list, name='article-list'),
    path('articles/<str:slug>/', views.ArticleDetailView.as_view(), name='article'),

    # Edit articles
    path('edit/create/', views.create_article, name='create-article'),
    path('edit/<str:uuid>/', views.edit_article, name='edit-article'),
    path('edit/<str:uuid>/delete/', views.delete_article, name='delete-article'),
    path('edit/<str:uuid>/upload-article-image', views.upload_article_image, name='upload-article-image'),

    # Comments
    path('article/<str:article_uuid>/comment/', views.add_comment, name='add-comment'),
    path('article/<str:article_uuid>/comments/<str:comment_uuid>/like/', views.toggle_comment_like,
         name='toggle-comment-like'),
    path('article/<str:article_uuid>/comments/<str:comment_uuid>/dislike/', views.toggle_comment_dislike,
         name='toggle-comment-dislike'),

    path('article/<str:article_uuid>/comments/<str:comment_uuid>/report/', views.ReportComment.as_view(),
         name='report-comment'),

    path('article/comments/<str:comment_uuid>/delete/', views.DeleteComment.as_view(),
         name='delete-comment'),

    # path('article/<str:article_uuid>/comment/<str:comment_uuid>/report/', views.report_comment, name='report-comment'),
    # path('article/<str:article_uuid>/comment/<str:comment_uuid>/delete/', views.delete_comment, name='delete-comment'),
]
