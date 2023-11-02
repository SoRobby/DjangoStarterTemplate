import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from django.db.models import Q


# Base views
class BaseAdminPanelTemplateView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_staff


class BaseAdminPanelListView(UserPassesTestMixin, ListView):
    paginate_by = 2
    PAGINATION_PAGES_BEFORE_AND_AFTER = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logging.debug('LIST VIEW CALLED')

        page_obj = context['page_obj']
        paginator = context['paginator']
        current_page = page_obj.number
        total_pages = paginator.num_pages

        start_page_num = (current_page - 1) * self.paginate_by + 1
        end_page_num = start_page_num + len(page_obj.object_list) - 1

        context['start_page'] = start_page_num
        context['end_page'] = end_page_num
        context['objects'] = page_obj
        context['page_range'] = range(
            max(1, current_page - self.PAGINATION_PAGES_BEFORE_AND_AFTER),
            min(total_pages, current_page + self.PAGINATION_PAGES_BEFORE_AND_AFTER) + 1
        )

        return context

    def test_func(self):
        return self.request.user.is_staff


class BaseAdminPanelSearchView(UserPassesTestMixin, TemplateView):
    model = None  # Should be overridden by subclass
    search_fields = None  # Default search fields, can be overridden
    search_key = 'list_search'

    def get_search_text(self):
        return self.request.GET.get(self.search_key, None)

    def get_queryset(self):
        search_text = self.get_search_text()

        if search_text:
            # Construct the Q objects for each search field
            query = Q()

            for field in self.search_fields:
                query |= Q(**{f'{field}__icontains': search_text})
            return self.model.objects.filter(query)
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_items'] = self.get_queryset()
        print(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def test_func(self):
        return self.request.user.is_staff


class BaseAdminPanelSearchListView(UserPassesTestMixin, ListView):
    model = None  # Should be overridden by subclass
    search_fields = []  # Default search fields, can be overridden. Should be a list
    search_key = 'list_search'
    paginate_by = 2
    PAGINATION_PAGES_BEFORE_AND_AFTER = 1

    def get_search_text(self):
        return self.request.GET.get(self.search_key, None)

    def get_queryset(self):
        search_text = self.get_search_text()
        logging.debug(f'search_text = {search_text}')

        if search_text:
            # Construct the Q objects for each search field
            query = Q()

            for field in self.search_fields:
                query |= Q(**{f'{field}__icontains': search_text})
            return self.model.objects.filter(query)
        else:
            return super().get_queryset()  # Call the parent class's get_queryset if no search_text

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = context['page_obj']
        paginator = context['paginator']
        current_page = page_obj.number
        total_pages = paginator.num_pages

        start_page_num = (current_page - 1) * self.paginate_by + 1
        end_page_num = start_page_num + len(page_obj.object_list) - 1

        context['start_page'] = start_page_num
        context['end_page'] = end_page_num
        context['list_items'] = page_obj
        context['page_range'] = range(
            max(1, current_page - self.PAGINATION_PAGES_BEFORE_AND_AFTER),
            min(total_pages, current_page + self.PAGINATION_PAGES_BEFORE_AND_AFTER) + 1
        )
        context[self.search_key] = self.get_search_text()  # Add the current search text to the context
        context['table_search'] = self.get_search_text()

        return context

    def test_func(self):
        return self.request.user.is_staff



