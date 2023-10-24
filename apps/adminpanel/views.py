import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.sessions.models import Session

from apps.feedback.models import Feedback
from libs.utils import ExportToCSVView

User = get_user_model()


# Create your views here.
def staff_or_admin(user):
    return user.is_staff or user.is_superuser


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_or_admin), name='dispatch')
class AdminPanelComponentsView(TemplateView):
    template_name = 'adminpanel/components.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_or_admin), name='dispatch')
class AdminPanelHomeView(TemplateView):
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


class AdminPanelFeedbackListView(UserPassesTestMixin, ListView):
    model = Feedback
    template_name = 'adminpanel/feedback/list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        PAGES_BEFORE_AND_AFTER = 1

        context = super().get_context_data(**kwargs)

        current_page = context['page_obj'].number
        total_pages = context['paginator'].num_pages

        # Calculate the start and end for the current page
        start_page = (context['page_obj'].number - 1) * self.paginate_by + 1
        end_page = start_page + len(context['page_obj'].object_list) - 1

        context['start_page'] = start_page
        context['end_page'] = end_page
        context['feedbacks_total'] = self.model.objects.all().count()
        context['feedbacks'] = context['page_obj']

        # Display up to 2 pages before and after the current page.
        start_page = max(1, current_page - PAGES_BEFORE_AND_AFTER)
        end_page = min(total_pages, current_page + PAGES_BEFORE_AND_AFTER)
        context['page_range'] = range(start_page, end_page + 1)
        return context

    def test_func(self):
        return self.request.user.is_staff


class AdminPanelFeedbackSearchView(TemplateView):
    template_name = 'adminpanel/feedback/partials/tbody.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('feedback_search', None)

        logging.debug(f'feedback_search: {search_text}')

        if search_text:
            feedbacks = Feedback.objects.filter(content__icontains=search_text)
        else:
            feedbacks = Feedback.objects.all()

        context['feedbacks'] = feedbacks
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


@method_decorator(staff_member_required, name='dispatch')
class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'adminpanel/feedback/view.html'
    context_object_name = 'feedback'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ExportFeedbacksToCSV(ExportToCSVView):
    model = Feedback
    filename = "feedbacks.csv"



# def delete_django_sessions(request):
#     Session.objects.all().delete()
#     return render(request, 'adminpanel/home.html')