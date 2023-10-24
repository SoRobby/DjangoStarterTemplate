from django.urls import path

# from . import views
from .views import views

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
    path('blog/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/<uuid:uuid>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/export/csv/', views.BlogExportToCSV.as_view(), name='blog-export-to-csv'),

    # Component URLs
    path('components/', views.AdminPanelComponentsView.as_view(), name='components'),
]
