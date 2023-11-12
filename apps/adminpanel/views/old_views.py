import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, DetailView
from django.utils import timezone, dateformat

from apps.blog.models import Article
from apps.feedback.models import Feedback
from .base_views import BaseAdminPanelTemplateView, BaseAdminPanelListView, BaseAdminPanelSearchListView
from apps.analytics.models import ObjectViewed
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear

from apps.core.utils import ExportToCSVView, ExportToTextView, ExportToJSONView

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

        # feedback_last_week_percent_change = Feedback.percent_change_last_week()
        feedback_last_week_percent_change = 'HARDCODED'

        logging.debug(f'feedback_last_week_percent_change: {feedback_last_week_percent_change}')

        context['users'] = users
        context['feedback_count'] = feedback_count
        context['feedback_last_week_percent_change'] = feedback_last_week_percent_change
        context['feedback'] = feedback
        return context




# Blog views
class BlogArticleListView(BaseAdminPanelListView):
    model = Article
    template_name = 'adminpanel/blog/list.html'


class BlogArticleDetailView(UserPassesTestMixin, DetailView):
    model = Article
    template_name = 'adminpanel/blog/detail.html'
    context_object_name = 'object'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(self.model)

        # Fetch related ObjectViewed items
        context['object_views'] = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id)

        unique_views = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).values(
            'user_session__session_key').annotate(count=Count('user_session__session_key')).count()

        # unique_views = (ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id)
        #                 .values('user_session__session_key', 'user_session__expire_date')
        #                 .annotate(count=Count('user_session__session_key'))
        #                 .count())

        context['unique_views'] = unique_views

        # Total views and unique views per day
        views_per_day = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).annotate(
            date=TruncDay('date_viewed')).values('date').annotate(total_views=Count('id'),
                                                                  unique_views=Count('user_session__session_key',
                                                                                     distinct=True))

        # Total views and unique views per week
        views_per_week = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).annotate(
            week=TruncWeek('date_viewed')).values('week').annotate(total_views=Count('id'),
                                                                   unique_views=Count('user_session__session_key',
                                                                                      distinct=True))

        # Total views and unique views per month
        views_per_month = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).annotate(
            month=TruncMonth('date_viewed')).values('month').annotate(total_views=Count('id'),
                                                                      unique_views=Count('user_session__session_key',
                                                                                         distinct=True))

        views_per_quarter = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).annotate(
            month=TruncQuarter('date_viewed')).values('month').annotate(total_views=Count('id'),
                                                                        unique_views=Count('user_session__session_key',
                                                                                           distinct=True))

        views_per_year = ObjectViewed.objects.filter(content_type=content_type, object_id=self.object.id).annotate(
            month=TruncYear('date_viewed')).values('month').annotate(total_views=Count('id'),
                                                                     unique_views=Count('user_session__session_key',
                                                                                        distinct=True))

        context['views_per_day'] = views_per_day
        context['views_per_week'] = views_per_week
        context['views_per_month'] = views_per_month
        context['views_per_quarter'] = views_per_quarter
        context['views_per_year'] = views_per_year

        return context

    def test_func(self):
        return self.request.user.is_staff


class BlogArticleExportToCSV(ExportToCSVView):
    model = Article
    filename = f'article {timezone.now().strftime("(%Y-%m-%d %H-%M-%S)")}.csv'


# Component views
class AdminPanelComponentsView(TemplateView):
    template_name = 'adminpanel/components.html'
