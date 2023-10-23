from collections import OrderedDict

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from .models import Feature


# Create your views here.
def roadmap(request):
    context = {}

    context['active_features'] = Feature.objects.filter(release_status='in_progress')
    context['planned_features'] = Feature.objects.filter(release_status='planned')
    context['archived_features'] = Feature.objects.filter(release_status='archived')

    # Query for released features grouped by month
    released_features_by_month = (
        Feature.objects
        .filter(release_status=Feature.ReleaseStatus.RELEASED)
        .annotate(month=TruncMonth('date_released'))
        .values('month')
        .annotate(feature_count=Count('id'))
        .filter(feature_count__gt=0)
        .order_by('-month')
    )

    # Convert to dictionary with month as key and list of features as value

    released_grouped_features = OrderedDict()
    for item in released_features_by_month:
        month = item['month']
        features = Feature.objects.filter(date_released__month=month.month, date_released__year=month.year)
        released_grouped_features[month.strftime('%B %Y')] = features

    context['released_grouped_features'] = released_grouped_features

    return render(request, 'roadmap/roadmap.html', context)
