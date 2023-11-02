from collections import OrderedDict

from django.views.generic import ListView

from .models import Feature


# Views
class RoadmapView(ListView):
    model = Feature
    template_name = 'roadmap/roadmap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        released_features_by_month = self.object_list.released_by_month()
        released_grouped_features = OrderedDict()

        for item in released_features_by_month:
            month = item['month']
            features = Feature.objects.filter(date_released__month=month.month, date_released__year=month.year)
            released_grouped_features[month.strftime('%B %Y')] = features

        context['active_features'] = Feature.objects.in_progress()
        context['planned_features'] = Feature.objects.planned()
        context['archived_features'] = Feature.objects.archived()
        context['released_grouped_features'] = released_grouped_features

        return context
