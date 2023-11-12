import logging

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from apps.feedback.models import Feedback
from .base_views import BaseAdminPanelTemplateView

User = get_user_model()


class AdminPanelHomeView(BaseAdminPanelTemplateView):
    template_name = 'adminpanel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admin Panel'

        # Get all users and date_created property
        users = User.objects.all().values('username', 'email', 'date_joined', 'is_staff', 'is_admin', 'is_superuser')
        feedback_count = Feedback.objects.filter(is_processed=False).count()
        feedback = Feedback.objects.all()

        # feedback_last_week_percent_change = Feedback.percent_change_last_week()
        feedback_last_week_percent_change = 'HARDCODED'

        logging.debug(f'feedback_last_week_percent_change: {feedback_last_week_percent_change}')

        context['users'] = users
        context['feedback_count'] = feedback_count
        context['feedback_last_week_percent_change'] = feedback_last_week_percent_change
        context['feedback'] = feedback
        return context


# Component views
class AdminPanelComponentsView(TemplateView):
    template_name = 'adminpanel/components.html'
