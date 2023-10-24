import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, DetailView
from django.utils import timezone, dateformat

from apps.blog.models import Article
from apps.feedback.models import Feedback
from libs.utils import ExportToCSVView
from .base_views import BaseAdminPanelTemplateView, BaseAdminPanelListView, BaseAdminPanelSearchListView

User = get_user_model()


# Views
class AdminPanelHomeView(BaseAdminPanelTemplateView):
    template_name = 'adminpanel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admin Panel'

        # Get all users and date_created property
        users = User.objects.all().values('username', 'email', 'date_joined', 'is_staff', 'is_admin', 'is_superuser')
        feedback_count = Feedback.objects.filter(is_processed=False).count()
        feedback = Feedback.objects.all()

        feedback_last_week_percent_change = Feedback.percent_change_last_week()

        logging.debug(f'feedback_last_week_percent_change: {feedback_last_week_percent_change}')

        context['users'] = users
        context['feedback_count'] = feedback_count
        context['feedback_last_week_percent_change'] = feedback_last_week_percent_change
        context['feedback'] = feedback
        return context


# Feedback view
class FeedbackListView(BaseAdminPanelSearchListView):
    model = Feedback
    template_name = 'adminpanel/feedback/list.html'
    search_fields = ['content']
    search_key = 'table_search'


class FeedbackSearchView(BaseAdminPanelSearchListView):
    model = Feedback
    template_name = 'adminpanel/feedback/partials/table-container.html'
    search_fields = ['content']
    search_key = 'table_search'


class FeedbacksExportToCSV(ExportToCSVView):
    model = Feedback
    filename = f'feedbacks {timezone.now().strftime("(%Y-%m-%d %H-%M-%S)")}.csv'


class FeedbackDetailView(UserPassesTestMixin, DetailView):
    model = Feedback
    template_name = 'adminpanel/feedback/view.html'
    context_object_name = 'feedback'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def test_func(self):
        return self.request.user.is_staff



# Blog views
class BlogListView(BaseAdminPanelListView):
    model = Article
    template_name = 'adminpanel/blog/list.html'


class BlogDetailView(UserPassesTestMixin, DetailView):
    model = Article
    template_name = 'adminpanel/blog/detail.html'
    context_object_name = 'object'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def test_func(self):
        return self.request.user.is_staff


class BlogExportToCSV(ExportToCSVView):
    model = Article
    filename = f'article {timezone.now().strftime("(%Y-%m-%d %H-%M-%S)")}.csv'



# Component views
class AdminPanelComponentsView(TemplateView):
    template_name = 'adminpanel/components.html'
