from django.urls import path

# from . import views
from . import views

# from .views import views
# from .views import *

app_name = 'adminpanel'

# Root url of "adminpanel" is '', defined in config.urls.py
urlpatterns = [
    path('home/', views.AdminPanelHomeView.as_view(), name='home'),

    # Feedback
    path('feedback/', views.FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/<uuid:uuid>/', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback/export/csv/', views.FeedbacksExportToCSV.as_view(), name='export-feedback-to-csv'),
    path('feedback/search/', views.FeedbackSearchView.as_view(), name='feedback-search'),

    # Blog
    path('blog/', views.BlogArticleListView.as_view(), name='blog-article-list'),
    path('blog/<uuid:uuid>/', views.BlogArticleDetailView.as_view(), name='blog-article-detail'),
    path('blog/export/csv/', views.BlogArticleExportToCSV.as_view(), name='blog-article-export-to-csv'),
    path('blog/export/json/', views.BlogArticleExportToJSON.as_view(), name='blog-article-export-to-json'),

    # Component URLs
    path('components/', views.AdminPanelComponentsView.as_view(), name='components'),
]
