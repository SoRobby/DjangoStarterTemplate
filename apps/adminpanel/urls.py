from django.urls import path

from . import views

app_name = 'adminpanel'

# Root url of "adminpanel" is '', defined in config.urls.py
urlpatterns = [
    path('home/', views.AdminPanelHomeView.as_view(), name='home'),

    # Feedback
    path('feedback/list/', views.AdminPanelFeedbackListView.as_view(), name='feedback-list'),
    path('feedback/list/<uuid:uuid>/', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback/search/', views.AdminPanelFeedbackSearchView.as_view(), name='feedback-search'),
    path('feedback/list/export/csv/', views.ExportFeedbacksToCSV.as_view(), name='export-feedback-to-csv'),

    # Blog
    path('blog/list/', views.AdminPanelBlogListView.as_view(), name='blog-list'),

    path('components/', views.AdminPanelComponentsView.as_view(), name='components'),
]
