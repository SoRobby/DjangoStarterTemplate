from django.urls import path

from . import views

app_name = 'adminpanel'

# Base url of the profile app is 'adminpanel' (/adminpanel/)
urlpatterns = [
    path('home/', views.AdminPanelHomeView.as_view(), name='home'),

    # Feedback
    path('feedback/list/', views.AdminPanelFeedbackListView.as_view(), name='feedback-list'),
    path('feedback/search/', views.AdminPanelFeedbackSearchView.as_view(), name='feedback-search'),
    # path('feedback/search/', views.feedback_search, name='feedback-search'),

    path('feedback/list/export/csv/', views.ExportFeedbacksToCSV.as_view(), name='export-feedback-to-csv'),

    path('components/', views.AdminPanelComponentsView.as_view(), name='components'),
]
