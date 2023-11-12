import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, DetailView
from django.utils import timezone

from apps.feedback.models import Feedback
from .base_views import BaseAdminPanelTemplateView, BaseAdminPanelListView, BaseAdminPanelSearchListView

from apps.core.utils import ExportToCSVView, ExportToTextView, ExportToJSONView

User = get_user_model()


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
    template_name = 'adminpanel/feedback/detail.html'
    context_object_name = 'feedback'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def test_func(self):
        return self.request.user.is_staff
